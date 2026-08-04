import json
from backend.skill_extractor import extract_skills_llm

# Same JD bank you used earlier
jd_bank = {

    "Frontend Developer": """
    HTML, CSS, JavaScript, React, Angular, responsive design,
    Bootstrap, UI/UX design, REST API integration.
    """,

    "Backend Developer": """
    Python, Java, Node.js, SQL, MySQL, PostgreSQL,
    REST APIs, authentication, databases, Git.
    """,

    "Python Developer": """
    Python, Django, Flask, APIs, SQL,
    Pandas, NumPy, backend development.
    """,

    "Data Scientist": """
    Python, Machine Learning, Pandas, NumPy,
    Scikit-learn, data visualization, statistics,
    predictive modeling, TensorFlow.
    """,

    "Full Stack Developer": """
    HTML, CSS, JavaScript, React, Node.js,
    Express, MongoDB, MySQL, REST APIs.
    """,

    "Mobile App Developer (iOS/Android)": """
    Android, iOS, Flutter, React Native,
    Java, Kotlin, Swift, Firebase.
    """,

    "Machine Learning Engineer": """
    Python, Machine Learning, Deep Learning,
    TensorFlow, PyTorch, NLP.
    """,

    "Cloud Engineer": """
    AWS, Azure, Docker, Kubernetes,
    CI/CD, Linux, networking.
    """
}

jd_skills = {}

print("Extracting JD skills...")

for role, jd_text in jd_bank.items():
    skills = extract_skills_llm(jd_text)
    jd_skills[role] = skills
    print(role, "->", skills)

# Save JSON
with open("jd_skills.json", "w") as f:
    json.dump(jd_skills, f, indent=4)

print("\nSaved jd_skills.json successfully!")