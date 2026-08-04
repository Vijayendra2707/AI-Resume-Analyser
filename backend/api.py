import os
import io # 🔴 Add this
from pathlib import Path
import pickle
import datetime
import traceback
import pandas as pd
from typing import List, Optional

from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# --- Security & Auth ---
from jose import JWTError, jwt
from backend.auth import (
    SECRET_KEY, ALGORITHM, get_password_hash, 
    verify_password, create_access_token
)

# --- Database Models & AI Utilities ---
# Ensure these match your existing files exactly
from backend.db import SessionLocal, engine, Base, User, AnalysisRecord, init_db
from backend.preprocess import preprocess_text
from backend.similarity import similarity_score
from backend.skill_extractor import extract_skills_llm
from backend.recommend import get_top_missing_skills, generate_course_links
from backend.utils import extract_text_from_pdf, extract_text_from_docx
from backend.report_generator import generate_resume_report

# 1. Initialize App & DB
app = FastAPI(title="AI Resume Screener Pro 2026")
init_db()

# Create folder for PDF reports
if not os.path.exists("reports"):
    os.makedirs("reports")

app.mount("/reports", StaticFiles(directory="reports"), name="reports")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For production, use ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. ML Model Loading
try:
    BASE_DIR = Path(__file__).resolve().parent
    MODEL_PATH = BASE_DIR / "model.pkl"

    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    FEATURES = ["similarity", "matched", "missing", "percent", "length"]

except Exception as e:
    print(f"⚠️ Model Warning: {e}. Predictive features may be disabled.")
# --- DEPENDENCIES ---

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# --- AUTH ENDPOINTS ---
def flatten_and_normalize(skills_dict):
    result = set()
    for sublist in skills_dict.values():
        for skill in sublist:
            result.add(preprocess_text(skill))
    return result


@app.post("/signup")
def signup(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user_exists = db.query(User).filter(User.email == email).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        email=email,
        hashed_password=get_password_hash(password),
        role="candidate"
    )
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": user.email})
    return {
        "access_token": access_token, 
        "token_type": "bearer", 
        "role": user.role,
        "email": user.email
    }

# --- CORE ANALYSIS ENDPOINT ---

@app.post("/analyze_resume")
async def analyze_resume(
    resume: UploadFile = File(...),
    jd_text: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    filename = resume.filename
    
    # 1. Extraction
    try:
        content = await resume.read()
        if not content:
            raise ValueError("Uploaded file is empty")
        
        # 🔴 THE FIX: Wrap bytes in io.BytesIO so pdfplumber can 'seek' through them
        file_stream = io.BytesIO(content) 

        if filename.endswith(".pdf"):
            resume_text = extract_text_from_pdf(file_stream) # Pass the stream, not raw content
        else:
            # docx handles bytes differently, but BytesIO is safer here too
            resume_text = extract_text_from_docx(file_stream) 
            
    except Exception as e:
        print(f"❌ Extraction failed: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Text extraction failed: {str(e)}")
    
    # 2. AI Skill Extraction
    resume_skills_dict = extract_skills_llm(resume_text)
    jd_skills_dict = extract_skills_llm(jd_text)

    # Flatten the resume skills into preprocessed strings
    all_res = flatten_and_normalize(resume_skills_dict)
    
    # --- 3. UPGRADED GAP ANALYSIS (Fixes Both Categories & Global Scoring) ---
    matched_set = set()
    missing_set = set()
    categorized_gap = {}

    for cat in ["technical_skills", "tools", "concepts"]:
        raw_jd_skills = jd_skills_dict.get(cat, [])
        cat_matched = []
        cat_missing = []

        for raw_skill in raw_jd_skills:
            clean_jd_skill = preprocess_text(raw_skill)
            
            # Smart Substring Match (handles LLM comma-separated strings)
            is_matched = False
            for clean_res_skill in all_res:
                if f" {clean_jd_skill} " in f" {clean_res_skill} ":
                    is_matched = True
                    break
            
            if is_matched:
                cat_matched.append(raw_skill) # For the UI/PDF
                matched_set.add(clean_jd_skill) # For the Math
            else:
                cat_missing.append(raw_skill) # For the UI/PDF
                missing_set.add(clean_jd_skill) # For the Math

        categorized_gap[cat] = {
            "matched": cat_matched,
            "missing": cat_missing
        }
    # 3. The Math (40/60 Split)
    # Raw Score = (Similarity * 40) + (Skill Match % * 60)
    sim = similarity_score(preprocess_text(resume_text), preprocess_text(jd_text))
    total_jd_skills = len(matched_set) + len(missing_set)
    match_pct = len(matched_set) / ((total_jd_skills) + 1e-5)
    
    sim_score = round(sim * 40, 2)
    skill_score = round(match_pct * 60, 2)
    raw_total = round(sim_score + skill_score, 2)

    # 4. ML Prediction
    length = len(preprocess_text(resume_text).split())
    features = pd.DataFrame([[sim, len(matched_set), len(missing_set), match_pct, length]], columns=FEATURES)
    
    shortlisted = int(model.predict(features)[0])
    confidence = round(max(model.predict_proba(features)[0]) * 100, 2)

    # 5. Fitment Index (UX Normalization)
    # We apply a rescaling for shortlisted candidates: 60 + (raw * 0.35)
    display_score = raw_total
    if shortlisted == 1:
        display_score = round(60 + (raw_total * 0.35), 2)
    display_score = min(display_score, 98.5)

    # 6. Reasoning & Suggestions
    reasons = []
    if shortlisted == 0:
        if sim < 0.35: reasons.append("• Low Semantic Alignment: Domain context mismatch.")
        if match_pct < 0.50: reasons.append(f"• Technical Skill Gap: Missing {len(missing_set)} core requirements.")
        if not reasons: reasons.append("• High Competitive Bar: Profile below model threshold.")
        final_reasoning = "\n".join(reasons)
    else:
        final_reasoning = "Potential Match: High core fit identified despite keyword gaps." if raw_total < 50 else "Strong alignment with role requirements."

    improvement = "Ready for interviews!"
    if missing_set:
        top = [s.upper() for s in list(missing_set)[:2]]
        improvement = f" Mastering {' and '.join(top)} will further boost your Fitment Index."

# 6.5 GENERATE RECOMMENDATION LINKS (The missing piece!)
    recommendations = {}
    if missing_set:
        # We take the top 3 missing skills to avoid cluttering the UI
        top_missing = list(missing_set)[:3] 
        recommendations = generate_course_links(top_missing)

    # 7. Construct Response (Update this dictionary)
    response = {
        "candidate_name": filename.rsplit('.', 1)[0],
        "shortlisted": shortlisted,
        "score": display_score,
        "raw_score": raw_total,
        "similarity": sim,
        "confidence": confidence,
        "breakdown": {"similarity_score": sim_score, "skill_score": skill_score},
        "reasoning": final_reasoning,
        "improvement_suggestion": improvement,
        "course_links": recommendations, # 🔴 ADD THIS LINE
        "categorized_skills": categorized_gap,
        "matched_skills": list(matched_set),
        "missing_skills": list(missing_set),
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    # 8. Report Generation & DB Persistence
    try:
        pdf_path = generate_resume_report(response)
        BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

        response["report_url"] = (
            f"{BASE_URL}/reports/{os.path.basename(pdf_path)}"
        )
        new_record = AnalysisRecord(
            user_id=current_user.id,
            candidate_name=response["candidate_name"],
            score=display_score,
            shortlisted=shortlisted,
            confidence=confidence,
            # Convert sets to lists so MySQL JSON column can accept them
            matched_skills=list(matched_set), 
            missing_skills=list(missing_set),
            report_url=response["report_url"] 
        )
        db.add(new_record)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Persistence Error: {e}")

    return response

# --- DATA RETRIEVAL ENDPOINTS ---

@app.get("/history")
def get_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role == "admin":
        return db.query(AnalysisRecord).order_by(AnalysisRecord.id.desc()).all()
    return db.query(AnalysisRecord).filter(AnalysisRecord.user_id == current_user.id).order_by(AnalysisRecord.id.desc()).all()

@app.get("/admin/analytics")
def get_analytics(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    records = db.query(AnalysisRecord).all()
    if not records: return {"total": 0, "rate": 0}
    
    shortlisted_count = len([r for r in records if r.shortlisted == 1])
    return {
        "total_screenings": len(records),
        "shortlist_rate": round((shortlisted_count / len(records)) * 100, 2)
    } 