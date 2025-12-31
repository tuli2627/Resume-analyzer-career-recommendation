from preprocess import clean_text


# -------------------- SKILL DATABASE --------------------
SKILLS = [
    "python", "java", "c", "c++", "sql",
    "html", "css", "javascript", "react",
    "django", "flask",
    "machine learning", "deep learning", "nlp",
    "tensorflow", "keras",
    "pandas", "numpy",
    "data analysis", "data visualization",
    "power bi", "tableau",
    "aws", "cloud computing",
    "docker", "kubernetes",
    "cyber security", "networking", "ethical hacking",
    "android", "kotlin"
]


# -------------------- SKILL GAP ANALYSIS --------------------
def analyze_skill_gap(resume_text, job_text):
    resume_text = clean_text(resume_text)
    job_text = clean_text(job_text)

    resume_tokens = set(resume_text.split())
    job_tokens = set(job_text.split())

    resume_skills = set()
    job_skills = set()

    for skill in SKILLS:
        words = skill.split()

        # single-word skill
        if len(words) == 1:
            if words[0] in resume_tokens:
                resume_skills.add(skill)
            if words[0] in job_tokens:
                job_skills.add(skill)

        # multi-word skill
        else:
            if all(word in resume_tokens for word in words):
                resume_skills.add(skill)
            if all(word in job_tokens for word in words):
                job_skills.add(skill)

    matched_skills = sorted(resume_skills & job_skills)
    missing_skills = sorted(job_skills - resume_skills)

    return matched_skills, missing_skills
