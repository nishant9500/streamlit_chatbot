import streamlit as st
from google.cloud import aiplatform

# ---------------------------
# GCP & Vertex AI Configuration
# ---------------------------
PROJECT_ID = "your-gcp-project-id"
LOCATION = "us-central1"  # or your model region
MODEL_NAME = "gemini-1.5-flash"  # Example Vertex AI generative model

aiplatform.init(project=PROJECT_ID, location=LOCATION)

# Load model
model = aiplatform.models.TextGenerationModel.from_pretrained(MODEL_NAME)

# ---------------------------
# Streamlit UI Setup
# ---------------------------
st.set_page_config(page_title="Vertex AI Chatbot", layout="centered")
st.title("💬 Vertex AI Chatbot")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User prompt
if prompt := st.chat_input("Ask me something..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response from Vertex AI
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = model.predict(prompt).text
            st.markdown(response)

    # Add assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": response})
