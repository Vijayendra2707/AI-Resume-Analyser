from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from resume_parser import extract_text
from preprocess import preprocess_text
from skill_extractor import extract_skills_llm
def similarity_score(resume_text, jd_text):
    tfidf = TfidfVectorizer()
    vectors = tfidf.fit_transform([resume_text, jd_text])

    score = cosine_similarity(vectors[0], vectors[1])

    return score[0][0]

def skill_match_score(resume_skills, jd_skills):
    # Convert lists to Python sets for easy math
    resume_set = set(resume_skills)
    jd_set = set(jd_skills)
    
    # Find the skills that exist in BOTH sets
    matched_skills = resume_set.intersection(jd_set)
    
    # Calculate the percentage of JD skills the candidate has
    if len(jd_set) == 0:
        return 0.0
        
    score = len(matched_skills) / len(jd_set)
    return round(score * 100, 2) # Returns a clean percentage like 85.5%

def calculate_final_score(context_score_raw, skill_score_percent):
    # Convert the 0.14 raw score into 14.35%
    context_score_percent = context_score_raw * 100
    
    # Define how much we care about each metric
    weight_skills = 0.70  # Hard skills make up 70% of the final grade
    weight_context = 0.30 # Overall vibe/context makes up 30%
    
    # Blend them together
    final_score = (skill_score_percent * weight_skills) + (context_score_percent * weight_context)
    
    return round(final_score, 2)

x = extract_text(r"C:\Users\ranev\Desktop\Vijayendra_Rane_Resume.docx")
y = preprocess_text(x)
z=extract_skills_llm(y)
jd="""
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
jd_clean=preprocess_text(jd)
a1=similarity_score(y,jd_clean)

jd_skills=extract_skills_llm(jd)
a2=skill_match_score(extract_skills_llm(x),jd_skills)
# print(a1,"   ",a2)
# print(calculate_final_score(a1,a2))