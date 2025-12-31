import pickle
import numpy as np
from preprocess import clean_text

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

def predict_jobs_from_skills(text, top_n=3):
    cleaned = clean_text(text)
    vec = vectorizer.transform([cleaned])

    probs = model.predict_proba(vec)[0]
    classes = model.classes_

    top_indices = np.argsort(probs)[::-1][:top_n]
    return [classes[i] for i in top_indices]
