import pandas as pd, joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

df = pd.read_csv("data/combined.csv")
train, test = train_test_split(df, test_size=0.2, stratify=df.label, random_state=42)

vec = TfidfVectorizer(lowercase=True, ngram_range=(1, 2), min_df=2)
clf = LogisticRegression(max_iter=1000, class_weight="balanced")
clf.fit(vec.fit_transform(train.text), train.label)

pred = clf.predict(vec.transform(test.text))
print(classification_report(test.label, pred, target_names=["normal", "scam"]))

ind = test[test.source == "indian"]
ind_pred = clf.predict(vec.transform(ind.text))
print("Indian scams in test set:", len(ind), "| caught:", int(ind_pred.sum()))

joblib.dump(vec, "models/vec.pkl")
joblib.dump(clf, "models/clf.pkl")
print("Saved model files.")