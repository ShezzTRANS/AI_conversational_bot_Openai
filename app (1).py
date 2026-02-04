import streamlit as st
from openai import OpenAI
import os

# --------------------------------------------------
# API KEY HANDLING (Streamlit-safe)
# --------------------------------------------------
api_key = None

# 1. Streamlit Secrets (Streamlit Cloud)
if hasattr(st, "secrets") and "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]

# 2. Environment variable fallback (local / Colab)
if not api_key:
    api_key = os.getenv("OPENAI_API_KEY")

# 3. Fail gracefully if missing
if not api_key:
    st.error("❌ OpenAI API key not found. Set OPENAI_API_KEY in Streamlit Secrets or environment variables.")
    st.stop()

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

SYSTEM_PROMPT = """You are a friendly and intelligent AI assistant designed to help users with a wide variety of tasks.

- Be clear, respectful, and helpful
- Ask clarifying questions when needed
- Do not request sensitive personal information
"""

st.title("🤖 Conversational Chatbot")
st.caption("Powered by AI | Education")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

prompt = st.chat_input("Type your message...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages
    )

    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.markdown(reply)

    MAX_MESSAGES = 20
    st.session_state.messages = (
        [st.session_state.messages[0]] +
        st.session_state.messages[-MAX_MESSAGES:]
    )
