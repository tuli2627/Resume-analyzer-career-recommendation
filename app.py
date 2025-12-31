from flask import Flask, render_template, request
import os
import PyPDF2
import nltk

from predictor import predict_jobs_from_skills
from skill_gap import analyze_skill_gap

# Download required NLTK resources safely
nltk.download("stopwords")
nltk.download("punkt")
nltk.download("punkt_tab")

app = Flask(__name__)


# -------------------- PDF TEXT EXTRACTION --------------------
def extract_text_from_pdf(pdf_file):
    text = ""
    reader = PyPDF2.PdfReader(pdf_file)
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()


# -------------------- HOME PAGE --------------------
@app.route("/", methods=["GET", "POST"])
def index():
    jobs = []
    matched_skills = []
    missing_skills = []

    # -------- SKILL → JOB RECOMMENDATION --------
    if request.method == "POST" and "skills" in request.form:
        skills = request.form.get("skills")
        if skills.strip():
            jobs = predict_jobs_from_skills(skills)

    return render_template(
        "index.html",
        jobs=jobs,
        matched_skills=matched_skills,
        missing_skills=missing_skills
    )


# -------------------- RESUME ANALYZER --------------------
@app.route("/resume-analyze", methods=["POST"])
def resume_analyze():
    jobs = []

    resume_pdf = request.files.get("resume_pdf")
    job_pdf = request.files.get("job_pdf")

    if not resume_pdf or not job_pdf:
        return render_template(
            "index.html",
            error="Please upload both Resume and Job Description PDFs."
        )

    resume_text = extract_text_from_pdf(resume_pdf)
    job_text = extract_text_from_pdf(job_pdf)

    matched_skills, missing_skills = analyze_skill_gap(resume_text, job_text)

    return render_template(
        "index.html",
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        jobs=jobs
    )


# -------------------- RUN APP --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
