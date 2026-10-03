from src.analyzer import analyze, risk_score, verdict

MESSAGES = [
    "Hi, this is Ravi from the courier. I'm outside your gate, please come and collect your package.",
    "Reminder: your electricity bill of Rs 1,150 is due on 10 Oct. Pay via the official app or at the counter.",
    "Hey, are we still meeting for dinner tonight? Mom said she will pick you up at 5.",
    "Your bank account statement for September is ready. Download it from the app or visit your branch.",
    "Rs 2,000 has been credited to your bank account ending 4821. Thank you for banking with us.",
    "Congratulations! Your mobile number has won Rs 5 crore in the WhatsApp international lottery. Reply with your name and bank account.",
    "Dear user, your Bank of Baroda account has been temporarily limited. Complete re-KYC at http://bob-rekyc.top within 2 hours.",
    "Your Netflix subscription failed. Update payment details at http://netflix-billing.in.net to avoid cancellation.",
]

for m in MESSAGES:
    s = risk_score(analyze(m))
    print(s, verdict(s), "|", m[:55])