import re

URL_RE = re.compile(r"https?://\S+|www\.\S+", re.I)
PHONE_RE = re.compile(r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)")
AMOUNT_RE = re.compile(r"(?:\u20b9|rs\.?|inr)\s?[\d,]+(?:\.\d+)?", re.I)

BRANDS = ["sbi", "hdfc", "icici", "axis", "kotak", "pnb", "paytm", "phonepe",
          "google pay", "gpay", "amazon", "flipkart", "jio", "airtel", "fedex",
          "dtdc", "india post", "aadhaar", "pan", "upi", "kyc", "otp", "cvv"]

URGENCY = ["immediately", "urgent", "urgently", "today", "right now", "act now",
           "last chance", "final notice", "blocked", "suspended", "expire",
           "disconnected", "within 24 hours", "within 1 hour", "avoid",
           "verify", "limited time", "arrest", "legal action"]


def analyze_features(text):
    low = text.lower()
    brands = [b for b in BRANDS if re.search(r"\b" + re.escape(b) + r"\b", low)]
    urgency = [u for u in URGENCY if u in low]
    return {
        "urls": URL_RE.findall(text),
        "phones": PHONE_RE.findall(text),
        "amounts": AMOUNT_RE.findall(text),
        "brands": brands,
        "urgency_words": urgency,
        "urgency_score": len(urgency),
    }