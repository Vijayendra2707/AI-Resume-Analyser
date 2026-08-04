import pandas as pd
import random
# Ensure these imports match your filenames exactly
from backend.similarity import similarity_score, skill_match_score
from backend.skill_extractor import extract_skills_llm
from backend.preprocess import preprocess_text
from backend.skill_gap import skill_gap

# 1. Load and Sample
df = pd.read_csv("updated_dataset.csv")

# We sample 250 rows to get 500 final rows (250 pos + 250 neg)
df_test = df.sample(n=100, random_state=42).reset_index(drop=True)

engineered_data = []

def get_features(res_text, jd_text):
    # PREPROCESS once for efficiency
    res_clean = preprocess_text(res_text)
    jd_clean = preprocess_text(jd_text)
    
    # CALCULATE Similarity (TF-IDF)
    # Using your imported similarity_score function
    sim_val = similarity_score(res_clean, jd_clean)

    # EXTRACT Skills (LLM)
    # Hint: Calling LLM 3 times per pair is slow. 
    # Here we consolidate to 2 calls.
    resume_skills = extract_skills_llm(res_text)
    jd_skills = extract_skills_llm(jd_text)

    # CALCULATE Match Score (Percentage)
    skill_score = skill_match_score(resume_skills, jd_skills)

    # CALCULATE Gap (Matched vs Missing)
    mat, mis = skill_gap(resume_skills, jd_skills)

    # RETURN the 5 features as a list
    # FIX: Use 'sim_val' (variable) not 'similarity_score' (function name)
    return [sim_val, len(mat), len(mis), skill_score, len(res_text)]

# 2. Loop Through the 250 Sampled Resumes
for i in range(len(df_test)):
    res_i = df_test.iloc[i]['Resume_Text']
    jd_i = df_test.iloc[i]['Target_Job_Description']
    
    # CREATE POSITIVE PAIR (Label 1)
    try:
        pos_features = get_features(res_i, jd_i)
        engineered_data.append(pos_features + [1])

        # CREATE NEGATIVE PAIR (Label 0)
        # Pick a random JD from the same sampled dataframe
        j = random.choice([x for x in range(len(df_test)) if x != i])
        jd_j = df_test.iloc[j]['Target_Job_Description']
        
        neg_features = get_features(res_i, jd_j)
        engineered_data.append(neg_features + [0])
        
        print(f"Processed Resume {i+1}/100 (Total Rows: {len(engineered_data)})")
        
    except Exception as e:
        print(f"Error at index {i}: {e}")
        continue

# 3. Final CSV Save
output_df = pd.DataFrame(engineered_data, columns=["similarity", "matched", "missing", "percent", "length", "label"])
output_df.to_csv("universal_training_data_200.csv", index=False)

print("\n✅ Success! File saved with 500 rows.")