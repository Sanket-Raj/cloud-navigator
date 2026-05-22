import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

st.set_page_config(page_title="CloudNavigator", layout="centered")
st.title("☁️ CloudNavigator – Multi-Cloud Migration Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask me about cloud migration..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        resp = requests.post(f"{BACKEND_URL}/chat", json={"message": prompt})
        if resp.status_code == 200:
            data = resp.json()
            reply = data["reply"]
            if data.get("runbook"):
                reply += "\n\n**Runbook:**\n" + "\n".join(f"- {s}" for s in data["runbook"]["steps"])
            if data.get("cost_comparison") and "message" not in data["cost_comparison"]:
                cc = data["cost_comparison"]
                reply += f"\n\n**Cost:** {cc['source_cloud']} ~${cc['source_estimated_monthly']}/mo, {cc['target_cloud']} ~${cc['target_estimated_monthly']}/mo (Savings: {cc['savings']})"
            if data.get("risk_score"):
                reply += f"\n\n**Risk:** {data['risk_score']['level']} – {', '.join(data['risk_score']['factors'])}"
        else:
            reply = f"Backend error: {resp.text}"
    except Exception as e:
        reply = f"Connection error: {str(e)}"

    with st.chat_message("assistant"):
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
