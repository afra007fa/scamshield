import pandas as pd

uci = pd.read_csv("data/SMSSpamCollection", sep="\t", names=["label", "text"])
nus = pd.read_csv("data/clean_nus_sms.csv")
indian = pd.read_csv("data/indian_scams.csv")
safe = pd.read_csv("data/indian_safe.csv")

# Scam class
uci_spam = uci[uci.label == "spam"][["text"]].assign(label=1, source="uci_spam")
indian_df = indian[["text"]].assign(label=1, source="indian")

# Normal class
uci_ham = uci[uci.label == "ham"][["text"]].sample(1500, random_state=42)
uci_ham = uci_ham.assign(label=0, source="uci_ham")

nus_ok = nus[["Message"]].rename(columns={"Message": "text"})
nus_ok["text"] = nus_ok["text"].astype(str).str.replace("<#>", "", regex=False).str.strip()
nus_ok = nus_ok[nus_ok["text"].str.len() >= 15].drop_duplicates()
nus_ok = nus_ok.sample(1500, random_state=42).assign(label=0, source="nus")

# Remove duplicates first, then add the repeated safe messages
df = pd.concat([uci_spam, indian_df, uci_ham, nus_ok])
df = df.drop_duplicates(subset="text")

safe_df = safe[["text"]].assign(label=0, source="indian_safe")
safe_df = pd.concat([safe_df] * 5)  # repeat so the model notices them

df = pd.concat([df, safe_df]).sample(frac=1, random_state=42)
df.to_csv("data/combined.csv", index=False, encoding="utf-8")

print(df.shape)
print(df.label.value_counts())
print(df.source.value_counts())