from ml_model import predict
from resume_parser import extract_text
from preprocess import preprocess_text
from similarity import similarity_score, skill_match_score
from skill_extractor import extract_skills_llm
from skill_gap import skill_gap

# The array MUST match the order: [similarity, matched_skills, missing_skills, resume_length]
x = extract_text(r"C:\Users\ranev\Desktop\Ananya_Sharma_Resume.pdf")
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
sim_score=similarity_score(y,jd_clean)

jd_skills=extract_skills_llm(jd)
skill_score=skill_match_score(extract_skills_llm(x),jd_skills)

resume_skills = extract_skills_llm(x)

# 2. Process JD
jd_skills = extract_skills_llm(jd)

# 3. Calculate Gap
mat, mis = skill_gap(resume_skills, jd_skills)

my_features = [sim_score, len(mat), len(mis),skill_score, len(x)]

# print(f"Testing model with features: {my_features}")

# Feed it to your trained AI brain!
result = predict(my_features)
# print(sim_score)
print("-" * 30)
if result == 1:
    print("🎯 PREDICTION: SHORTLISTED! Your model accepted you!")
else:
    print("❌ PREDICTION: REJECTED! Your model says you need more skills.")
    
    top_missing = get_top_missing_skills(mis)
    courses = generate_course_links(top_missing)

    print("\nRecommended Courses:")
    for skill, links in courses.items():
        print(f"\nSkill: {skill}")
        for platform, link in links.items():
            print(f"{platform}: {link}")
print("-" * 30)

"""Position: Electrical Engineer (Entry-Level)
Location: Pune, Maharashtra

We are looking for a motivated Electrical Engineer with strong fundamentals in electrical systems, circuit design, and basic automation. The ideal candidate should have hands-on experience with MATLAB, PLC programming, and embedded systems.

Responsibilities:
- Assist in designing and maintaining electrical systems and circuits
- Work with electrical machines and power systems
- Support PLC-based automation projects
- Perform testing and troubleshooting of electrical equipment
- Develop electrical drawings using AutoCAD Electrical
- Work on embedded systems and microcontroller-based projects
- Assist in industrial electrical maintenance tasks
- Document technical work and reports

Required Skills:
MATLAB,
PLC Programming,
Electrical Machines,
Power Systems,
Circuit Design,
AutoCAD Electrical,
Embedded Systems,
Microcontrollers (Arduino),
Electrical Wiring,
Troubleshooting,
Basic Automation,
Control Systems (Basic),
Python (Basic)

Preferred:
Internship experience in electrical or industrial environment
Knowledge of IoT-based electrical systems
"""