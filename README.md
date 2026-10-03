# 🛡️ ScamShield

**Paste a suspicious SMS or WhatsApp message. ScamShield tells you if it is a scam, why, and what to do.**

🔗 **Live demo:** https://scamshield-india.streamlit.app/

## The problem

People in India lose money to fake KYC, UPI refund, electricity bill, parcel, job and loan-app messages. Most people cannot tell a scam from a real message until it is too late, and elderly users are hit hardest.

## What it does

1. You paste a message.
2. ScamShield gives a verdict (**Safe / Suspicious / Scam**) with a risk score out of 100.
3. It shows **why**: trigger words, pressure words ("blocked", "today", "midnight") and, for strong matches, the closest known scam type.
4. It extracts **risky details**: links (shown as plain text so nobody clicks them by accident), phone numbers, amounts and bank or brand names.
5. Gemini writes a plain-language explanation and three safety tips, including the cyber fraud helpline (1930).

## How it works

```
Message -> TF-IDF + Logistic Regression -> scam probability
        -> Pattern extraction (regex)    -> links, phones, amounts, brands
        -> Pressure-word and scam-phrase checks
        -> Cosine similarity             -> closest known scam type
        -> Combined risk score           -> Safe / Suspicious / Scam
        -> Gemini                        -> explanation and advice
```

**Scoring:** the model's probability is the base. Links, phone numbers, brand names, pressure words, scam phrases (such as "lottery" or "reply with") and a strong similarity match each add points. If a message has none of these signals, the model's guess is weighted down, which reduces false alarms on normal messages about deliveries and bills.

NLP techniques used: text preprocessing, TF-IDF word vectorization (unigrams and bigrams), logistic regression classification, pattern-based entity extraction, keyword-based urgency analysis, cosine similarity search, and LLM-generated explanations.

## Data

- UCI SMS Spam Collection (spam and normal messages)
- NUS SMS Corpus (casual normal messages)
- 43 hand-written Indian scam messages (KYC, UPI, lottery, electricity bill, job offer, loan app, parcel, bank OTP, fake authority)
- 35 hand-written Indian normal messages (deliveries, bank alerts, reminders), added to reduce false alarms

The large raw datasets are not stored in this repo. Download them from their original sources to retrain.

## Results (honest numbers)

- **97% accuracy** on 758 held-out messages (scam recall 93%, scam precision 91%).
- Some repeated normal messages can appear in both the training and test sets, so this score is slightly optimistic.
- The scoring rules (signal weights, scam phrases, the weight-down rule) were tuned by hand while looking at about a dozen example messages. They are not validated on a large independent test set.
- The Indian examples are small and written by me, so real-world accuracy on new local scams will be lower.

## Limitations

- Trained on public SMS data plus a small hand-written Indian set. It can miss new scam styles, especially ones with no link, phone number or pressure words.
- Genuine messages that look like scams (for example, a real bank alert) can still be marked Suspicious or Scam.
- Messages are mostly English. Regional languages and mixed-language text are not supported yet.
- The AI explanation needs the Gemini API. If it is busy, the app retries, then falls back to the analysis alone.
- It is a helper, not a guarantee. Never share OTPs or PINs.

## Run it locally

```
git clone https://github.com/afra007fa/scamshield.git
cd scamshield
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file with your key (get a free one at aistudio.google.com):

```
GEMINI_API_KEY=your-key-here
```

Then run:

```
python -m streamlit run app.py
```

To retrain the model, put `SMSSpamCollection` and `clean_nus_sms.csv` in `data/`, then run `python src/build_data.py` and `python src/model.py`.

## Tech stack

Python, scikit-learn, pandas, Streamlit, Google Gemini API, Git and GitHub.

## Project structure

```
scamshield/
├── app.py              Streamlit app
├── src/
│   ├── features.py     links, phones, amounts, pressure words, scam phrases
│   ├── analyzer.py     model, trigger words, similarity, risk score
│   ├── explain.py      Gemini explanation with retries
│   ├── build_data.py   combines datasets
│   ├── model.py        trains the classifier
│   └── check_messages.py  quick sanity check on sample messages
├── data/               Indian scam and normal message sets
└── models/             saved model files
```

## Future work

- Collect more real Indian scam and normal messages, and validate on a separate test set
- Support Hindi, Tamil and mixed-language messages
- Let users report new scams to improve the dataset

## Educational use

Built for the AI Innovation Challenge as a learning project. Datasets belong to their original owners.