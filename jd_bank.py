import pandas as pd
import random
import time

from preprocess import preprocess_text
from skill_extractor import extract_skills_llm
from similarity import similarity_score, skill_match_score
from skill_gap import skill_gap

# ---------------- JD BANK ----------------
jd_bank = {

    "Frontend Developer": """
    Looking for a Frontend Developer skilled in HTML, CSS, JavaScript,
    React, Angular, responsive design, Bootstrap, UI/UX design,
    REST API integration, and web performance optimization.
    """,

    "Backend Developer": """
    Hiring a Backend Developer with experience in Python, Java, Node.js,
    SQL, MySQL, PostgreSQL, REST APIs, authentication, databases,
    server-side logic, Git, and backend architecture.
    """,

    "Python Developer": """
    Python Developer with Python, Django, Flask, APIs, SQL,
    Pandas, NumPy, object-oriented programming, debugging,
    backend development, and scripting.
    """,

    "Data Scientist": """
    Data Scientist with Python, Machine Learning, Pandas, NumPy,
    Scikit-learn, data visualization, statistics, data cleaning,
    predictive modeling, TensorFlow, and data analysis.
    """,

    "Full Stack Developer": """
    Full Stack Developer with HTML, CSS, JavaScript, React,
    Node.js, Express, MongoDB, MySQL, REST APIs, Git,
    frontend and backend development.
    """,

    "Mobile App Developer (iOS/Android)": """
    Mobile App Developer with Android, iOS, Flutter, React Native,
    Java, Kotlin, Swift, mobile UI design, API integration,
    Firebase, and mobile application development.
    """,

    "Machine Learning Engineer": """
    Machine Learning Engineer with Python, Machine Learning,
    Deep Learning, TensorFlow, PyTorch, Scikit-learn,
    data preprocessing, model training, NLP, and AI development.
    """,

    "Cloud Engineer": """
    Cloud Engineer with AWS, Azure, Google Cloud, Docker,
    Kubernetes, CI/CD, Linux, networking, cloud deployment,
    and DevOps tools.
    """
}
# ---------------- PRECOMPUTE JD SKILLS ----------------
print("Extracting JD skills...")
jd_skills_bank = {}
for cat, jd_text in jd_bank.items():
    jd_skills_bank[cat] = extract_skills_llm(jd_text)
print("JD skills extracted.\n")

# ---------------- FEATURE FUNCTION ----------------
def get_engineered_features(res_text, jd_text, res_skills, jd_skills):
    clean_res = preprocess_text(res_text)
    clean_jd = preprocess_text(jd_text)

    sim_val = similarity_score(clean_res, clean_jd)

    match_pct = skill_match_score(res_skills, jd_skills)
    matched, missing = skill_gap(res_skills, jd_skills)

    return [sim_val, len(matched), len(missing), match_pct, len(clean_res)]

# ---------------- LOAD DATASET ----------------
df = pd.read_csv("dataset/gpt_dataset.csv")

# Keep only categories present in JD bank
df = df[df['Category'].isin(jd_bank.keys())].reset_index(drop=True)

# Sample resumes
df_sample = df.sample(n=250, random_state=42).reset_index(drop=True)

final_data = []

print(f"Starting dataset generation for {len(df_sample)} resumes...\n")

# ---------------- MATCHING LOOP ----------------
for i in range(len(df_sample)):
    category = df_sample.iloc[i]['Category']
    resume_raw = df_sample.iloc[i]['Resume']

    # Skip very short resumes
    if len(resume_raw) < 800:
        continue
        print(i)
    try:
        # Extract resume skills ONCE
        res_skills = extract_skills_llm(resume_raw)

        # -------- Positive Pair --------
        correct_jd = jd_bank[category]
        correct_jd_skills = jd_skills_bank[category]

        pos_feat = get_engineered_features(
            resume_raw,
            correct_jd,
            res_skills,
            correct_jd_skills
        )
        final_data.append(pos_feat + [1])

        # -------- Negative Pair --------
        wrong_cat = random.choice([c for c in jd_bank.keys() if c != category])
        wrong_jd = jd_bank[wrong_cat]
        wrong_jd_skills = jd_skills_bank[wrong_cat]

        neg_feat = get_engineered_features(
            resume_raw,
            wrong_jd,
            res_skills,
            wrong_jd_skills
        )
        final_data.append(neg_feat + [0])

        print(f"Processed {i+1}/100 | Category: {category}")
        time.sleep(1)

    except Exception as e:
        print(f"Error at index {i}: {e}")
        continue

# ---------------- SAVE DATASET ----------------
output_cols = ["similarity", "matched", "missing", "percent", "length", "label"]
training_df = pd.DataFrame(final_data, columns=output_cols)
training_df.to_csv("universal_training_data_500.csv", index=False)

print("\nDataset created successfully!")
print("Rows generated:", len(training_df))