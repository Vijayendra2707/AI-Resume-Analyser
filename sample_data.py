import pandas as pd

# Load full datasets
resume_df = pd.read_csv("dataset/Resume.csv")
job_df = pd.read_csv("dataset/jobs.csv")

# Sample datasets
resume_sample = resume_df.sample(500, random_state=42)
job_sample = job_df.sample(200, random_state=42)

# Save sampled datasets
resume_sample.to_csv("resume_sample.csv", index=False)
job_sample.to_csv("job_sample.csv", index=False)

print("Sample datasets created!")