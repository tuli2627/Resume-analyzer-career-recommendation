import pandas as pd

# Load dataset once
df = pd.read_csv("resume_data.csv")

def recommend_skills(job_role):
    """
    Given a job role, return required skills
    """
    job_role = job_role.lower().strip()

    row = df[df["job_role"].str.lower() == job_role]

    if row.empty:
        return []

    skills_text = row.iloc[0]["resume_text"]
    skills = skills_text.split()

    return list(set(skills))
