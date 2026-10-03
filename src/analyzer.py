import joblib
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from src.features import analyze_features

vec = joblib.load("models/vec.pkl")
clf = joblib.load("models/clf.pkl")

_indian = pd.read_csv("data/indian_scams.csv")
_indian_matrix = vec.transform(_indian.text)
_feature_names = np.array(vec.get_feature_names_out())

STOP = {"your", "you", "the", "to", "a", "is", "of", "and", "in", "for", "on",
        "at", "it", "we", "our", "or", "be", "this", "that", "with", "are",
        "will", "has", "have", "from", "by", "now", "rs", "inr", "please"}


def _is_noise(word):
    return all(t in STOP or t.isdigit() for t in word.split())


def trigger_words(text, top_n=5):
    x = vec.transform([text])
    contrib = x.multiply(clf.coef_[0]).toarray()[0]
    words = []
    for i in np.argsort(contrib)[::-1]:
        if contrib[i] <= 0:
            break
        w = _feature_names[i]
        if _is_noise(w):
            continue
        words.append(w)
        if len(words) == top_n:
            break
    return words


def closest_scam(text):
    sims = cosine_similarity(vec.transform([text]), _indian_matrix)[0]
    best = int(np.argmax(sims))
    return {
        "scam_type": _indian.scam_type.iloc[best],
        "similarity": round(float(sims[best]), 2),
        "example": _indian.text.iloc[best],
    }


def analyze(text):
    prob = float(clf.predict_proba(vec.transform([text]))[0][1])
    return {
        "probability": round(prob, 3),
        "trigger_words": trigger_words(text),
        "closest": closest_scam(text),
        **analyze_features(text),
    }


def risk_score(result):
    score = result["probability"] * 100
    score += min(result["urgency_score"], 3) * 4
    if result["urls"]:
        score += 8
    if result["phones"]:
        score += 4
    if result["brands"]:
        score += 4
    if result["closest"]["similarity"] >= 0.4:
        score += 5
    return min(round(score), 100)


def verdict(score):
    if score >= 60:
        return "Scam"
    if score >= 35:
        return "Suspicious"
    return "Safe"