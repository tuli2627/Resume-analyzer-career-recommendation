import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Load dataset
data = pd.read_csv("resume_data.csv")

# Text cleaning
stop_words = set(stopwords.words("english"))

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z ]", " ", text)
    words = text.split()
    words = [w for w in words if w not in stop_words]
    return " ".join(words)

data["clean_text"] = data["resume_text"].apply(clean_text)

# Vectorization
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data["clean_text"])
y = data["job_role"]

# Train model
model = MultinomialNB()
model.fit(X, y)

def predict_job(resume_text):
    resume_text = clean_text(resume_text)
    resume_vector = vectorizer.transform([resume_text])
    prediction = model.predict(resume_vector)[0]

    return {
        "Predicted Role": prediction
    }
def resume_analyze(resume_text):
    cleaned = clean_text(resume_text)
    vector = vectorizer.transform([cleaned])
    job = model.predict(vector)[0]

    resume_words = set(cleaned.split())
    required_skills = set(
        data[data["job_role"] == job]["resume_text"].iloc[0].split()
    )

    missing_skills = list(required_skills - resume_words)

    return job, missing_skills
