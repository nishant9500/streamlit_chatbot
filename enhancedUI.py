import streamlit as st
import time
from agent import GeminiAgent

# -----------------------
# Config
# -----------------------
PROJECT_ID = "your-gcp-project-id"
LOCATION = "us-central1"

agent = GeminiAgent(PROJECT_ID, LOCATION)

# -----------------------
# Streamlit Page Setup
# -----------------------
st.set_page_config(page_title="Gemini Agent Chatbot", layout="wide")

# Header
st.markdown("""
    <h1 style='text-align: center; color: #2F80ED;'>🤖 Gemini Agent Chatbot</h1>
    <p style='text-align: center; font-size:16px; color: gray;'>Ask questions about your data or general topics</p>
""", unsafe_allow_html=True)

# Sidebar settings
with st.sidebar:
    st.header("⚙️ Settings")
    memory_mode = st.radio("Conversation Mode:", ("Memory ON", "Memory OFF"))
    start_new = st.button("Start New Session")

# Handle session reset
if start_new:
    st.session_state.clear()
    st.session_state.memory_on = (memory_mode == "Memory ON")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "memory_on" not in st.session_state:
    st.session_state.memory_on = (memory_mode == "Memory ON")

# Update memory mode
st.session_state.memory_on = (memory_mode == "Memory ON")

# -----------------------
# CSS for chat bubbles
# -----------------------
st.markdown("""
    <style>
    .chat-bubble-user {
        background-color: #DCF8C6;
        padding: 10px 15px;
        border-radius: 20px;
        margin: 5px 0;
        max-width: 70%;
        float: right;
        clear: both;
    }
    .chat-bubble-assistant {
        background-color: #F1F0F0;
        padding: 10px 15px;
        border-radius: 20px;
        margin: 5px 0;
        max-width: 70%;
        float: left;
        clear: both;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------
# Function for typing animation
# -----------------------
def type_text(text, role):
    display = ""
    placeholder = st.empty()
    for char in text:
        display += char
        if role == "user":
            placeholder.markdown(f"<div class='chat-bubble-user'>🧑 {display}</div>", unsafe_allow_html=True)
        else:
            placeholder.markdown(f"<div class='chat-bubble-assistant'>🤖 {display}</div>", unsafe_allow_html=True)
        time.sleep(0.01)
    return placeholder

# -----------------------
# Display previous messages
# -----------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='chat-bubble-user'>🧑 {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-assistant'>🤖 {msg['content']}</div>", unsafe_allow_html=True)

# -----------------------
# User input
# -----------------------
if prompt := st.chat_input("Type your message..."):
    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    type_text(prompt, "user")

    # Get agent response
    with st.spinner("Thinking..."):
        reply = agent.get_response(st.session_state.messages, memory_on=st.session_state.memory_on)
        type_text(reply, "assistant")

    # Save assistant reply
    st.session_state.messages.append({"role": "assistant", "content": reply})
