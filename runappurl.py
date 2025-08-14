import streamlit as st

# -----------------------
# Config
# -----------------------
ADK_RUN_APP_URL = "https://<your-adk-run-app-url>"

st.set_page_config(page_title="ADK Agent Chatbot", layout="wide")
st.title("💬 ADK Agent Chatbot (Embedded)")

st.markdown("""
<p style='text-align:center; font-size:16px; color:gray;'>
Interact with your deployed ADK agent below.
</p>
""", unsafe_allow_html=True)

# Embed the ADK agent using iframe
st.markdown(f"""
<iframe src="{ADK_RUN_APP_URL}" width="100%" height="800px" style="border:1px solid #ccc; border-radius:10px;"></iframe>
""", unsafe_allow_html=True)
