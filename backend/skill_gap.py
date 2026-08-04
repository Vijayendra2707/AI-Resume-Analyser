import re
from backend.resume_parser import extract_text
from backend.preprocess import preprocess_text
from backend.skill_extractor import extract_skills_llm

def normalize_skill(skill):
    """
    Standardizes strings to ensure 'SQL.' matches 'sql' 
    and 'Pandas' matches 'pandas'.
    """
    skill = skill.lower().strip()
    # Remove punctuation (like the period in 'sql.')
    skill = re.sub(r'[^a-z0-9\s-]', '', skill)
    # Basic lemmatization: remove trailing 's' to match 'pandas' and 'panda'
    if skill.endswith('s') and len(skill) > 3:
        skill = skill[:-1]
    return skill

def skill_gap(resume_skills, jd_skills):
    # Create a mapping of normalized skills back to their original form
    # This ensures we don't lose the professional formatting
    norm_resume = {normalize_skill(s): s for s in resume_skills}
    norm_jd = {normalize_skill(s): s for s in jd_skills}
    
    # Calculate intersection and difference on the normalized sets
    matched_keys = set(norm_resume.keys()).intersection(set(norm_jd.keys()))
    missing_keys = set(norm_jd.keys()) - set(norm_resume.keys())

    # Convert back to original formatting for display
    matched = [norm_jd[k] for k in matched_keys]
    missing = [norm_jd[k] for k in missing_keys]

    return matched, missing

# --- TEST EXECUTION ---
jd_text = """
[Position: Machine Learning & Generative AI Intern
Location: Remote / Pune, Maharashtra
Type: Internship (3-6 Months)

About the Role:
We are seeking a highly motivated Machine Learning Intern to join our AI Research and Development team. You will work closely with senior data scientists to design, train, and deploy intelligent systems, with a strong focus on Large Language Models (LLMs) and computer vision. The ideal candidate is passionate about solving real-world problems using cutting-edge Generative AI techniques.

Key Responsibilities:

Design and implement Retrieval-Augmented Generation (RAG) pipelines for complex document analysis.

Develop, evaluate, and fine-tune Deep Learning models using modern frameworks.

Build robust backend REST APIs to serve machine learning models to production environments.

Collaborate with the team to containerize applications and deploy scalable solutions.

Clean, process, and analyze large datasets to improve model accuracy and probabilistic evaluation metrics.

Required Qualifications:

Currently pursuing a degree in Computer Science, Computer Engineering, or a related field.

Strong programming fundamentals in Python and SQL.

Hands-on experience with deep learning libraries such as PyTorch or TensorFlow.

Familiarity with NLP tools, LLMs (e.g., Llama, OpenAI), and the Hugging Face ecosystem.

Experience building web applications or APIs using FastAPI, Django, or Flask.

Solid understanding of vector search technologies (FAISS, Pinecone, or ChromaDB).

Proficiency in data manipulation and evaluation using Pandas, NumPy, and Scikit-Learn.

Bonus Skills:

Experience building interactive frontend dashboards using Streamlit.

Familiarity with containerization tools like Docker and Kubernetes.

Understanding of cloud platforms (AWS or Google Cloud Compute).

Knowledge of relational and NoSQL databases (MySQL, MongoDB).]
"""

# 1. Process Resume
res_path = r"C:\Users\ranev\Desktop\Vijayendra_Rane_Resume.pdf"
raw_res = extract_text(res_path)
clean_res = preprocess_text(raw_res)
resume_skills = extract_skills_llm(raw_res)

# 2. Process JD
jd_skills = extract_skills_llm(jd_text)

# 3. Calculate Gap
mat, mis = skill_gap(resume_skills, jd_skills)

# print(f"Matched ({len(mat)}): {mat}")
# print(f"Missing ({len(mis)}): {mis}")

# Calculation for your ML Model features
total_jd = len(mat) + len(mis)
match_percent = len(mat) / total_jd if total_jd > 0 else 0
# print(f"Match Score for ML: {match_percent:.2%}")