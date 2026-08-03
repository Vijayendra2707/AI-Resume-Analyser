import pandas as pd
import os
from skill_extractor import extract_skills_llm
from section_extractor import extract_relevant_section

resume_df = pd.read_csv("resume_sample.csv")

if os.path.exists("resume_skills.csv"):
    existing = pd.read_csv("resume_skills.csv")
    done_ids = set(existing["resume_id"])
    skills_data = existing.values.tolist()
else:
    done_ids = set()
    skills_data = []

for i in range(len(resume_df)):
    if i in done_ids:
        continue

    text = str(resume_df.loc[i, "Resume_str"])

    # HERE we use section extractor
    section = extract_relevant_section(text)

    print(f"Processing Resume {i+1}/{len(resume_df)}")

    skills = extract_skills_llm(section)
    skills_string = ",".join(skills)

    skills_data.append([i, skills_string])

    df = pd.DataFrame(skills_data, columns=["resume_id", "skills"])
    df.to_csv("resume_skills.csv", index=False)

print("Resume skills extraction completed!")