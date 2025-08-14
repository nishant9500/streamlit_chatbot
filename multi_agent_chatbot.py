import streamlit as st
from google import genai
from google.genai.types import GenerateContentConfig

# ——— GCP & Gemini Agent Setup ———
PROJECT_ID = "your-gcp-project-id"
LOCATION = "us-central1"

# Initialize the Gen AI client
client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
MODEL_ID = "gemini-2.0-flash-001"

# ——— Streamlit UI ———
st.set_page_config(page_title="Vertex AI Gemini Agent Chatbot", layout="centered")
st.title("💬 Gemini 2.0 Flash Agent Chatbot")

# Session controls: Reset or Continue conversation
if st.button("Start New Session"):
    st.session_state.clear()

# Initialize state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask me something..."):
    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Build full conversation context as a list of texts
    conversation = [
        f"{m['role'].capitalize()}: {m['content']}"
        for m in st.session_state.messages
    ]
    # Create input for the model
    full_input = "\n".join(conversation) + "\nAssistant:"
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            config = GenerateContentConfig()
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=full_input,
                config=config
            )
            reply = response.text
            st.markdown(reply)

    # Append model reply
    st.session_state.messages.append({"role": "assistant", "content": reply})
