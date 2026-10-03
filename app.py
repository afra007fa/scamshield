import streamlit as st
from src.analyzer import analyze, risk_score, verdict

st.set_page_config(page_title="ScamShield", page_icon="🛡️")

EX_KYC = "Dear customer, your SBI KYC has expired. Update now at http://sbi-kyc-update.xyz or your account will be blocked today."
EX_UPI = "Sir, Rs 2,000 was sent to you by mistake on PhonePe. Please return it urgently to 9876543210."
EX_SAFE = "Hey, are we still meeting for dinner tonight? Mom said she will pick you up at 5."


def set_msg(text):
    st.session_state.msg = text


st.title("🛡️ ScamShield")
st.caption("Paste a suspicious SMS or WhatsApp message and find out if it is a scam.")

st.write("Try an example:")
c1, c2, c3 = st.columns(3)
c1.button("Fake KYC", on_click=set_msg, args=(EX_KYC,))
c2.button("UPI scam", on_click=set_msg, args=(EX_UPI,))
c3.button("Normal message", on_click=set_msg, args=(EX_SAFE,))

text = st.text_area("Message", key="msg", height=150)

if st.button("Analyze", type="primary"):
    if not text.strip():
        st.warning("Please paste a message first.")
    else:
        r = analyze(text)
        score = risk_score(r)
        v = verdict(score)
        no_red_flags = not (r["urls"] or r["phones"] or r["urgency_words"])

        if v == "Scam":
            st.error(f"🚨 SCAM - risk score {score}/100")
        elif v == "Suspicious":
            st.warning(f"⚠️ SUSPICIOUS - risk score {score}/100")
            if no_red_flags:
                st.write(
                    "No links, phone numbers or urgent demands were found, so "
                    "this may be a normal message. Verify with the sender "
                    "through a trusted channel before acting."
                )
            else:
                st.write(
                    "This message has some warning signs. Do not click links "
                    "or share details until you have verified it."
                )
        else:
            st.success(f"✅ SAFE - risk score {score}/100")

        if v != "Safe":
            st.subheader("Why it was flagged")
            if r["trigger_words"]:
                st.write("**Trigger words:** " + ", ".join(r["trigger_words"]))
            if r["urgency_words"]:
                st.write("**Pressure words:** " + ", ".join(r["urgency_words"]))
            if r["closest"]["similarity"] >= 0.4:
                st.write(
                    f"**Closest known scam type:** {r['closest']['scam_type']} "
                    f"(match {r['closest']['similarity']})"
                )

        st.subheader("Details found in the message")
        st.write("**Links:** " + (", ".join(r["urls"]) or "none"))
        st.write("**Phone numbers:** " + (", ".join(r["phones"]) or "none"))
        st.write("**Amounts:** " + (", ".join(r["amounts"]) or "none"))
        st.write("**Brands mentioned:** " + (", ".join(r["brands"]) or "none"))

st.divider()
st.caption(
    "Limitations: trained on public SMS datasets plus 43 hand-written Indian "
    "scam examples. It can miss new scam styles. Never share OTPs or PINs."
)