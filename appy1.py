import streamlit as st
from openai import OpenAI
import os

# --------------------------------------------------
# SAFE API KEY HANDLING (STREAMLIT-CLOUD SAFE)
# --------------------------------------------------
api_key = None

# 1️⃣ Try Streamlit Secrets safely
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except Exception:
    api_key = None

# 2️⃣ Fallback to environment variable (local / Colab)
if not api_key:
    api_key = os.getenv("OPENAI_API_KEY")

# 3️⃣ Fail gracefully if still missing
if not api_key:
    st.error(
        "❌ OpenAI API key not found.\n\n"
        "• On Streamlit Cloud: add OPENAI_API_KEY in Secrets\n"
        "• Locally: export OPENAI_API_KEY in your environment"
    )
    st.stop()

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# --------------------------------------------------
# SYSTEM PROMPT
# --------------------------------------------------
SYSTEM_PROMPT = """You are a friendly and intelligent AI assistant designed to help users with a wide variety of tasks.

CORE BEHAVIOR:
- Be clear, respectful, and helpful
- Ask clarifying questions when needed
- Explain concepts step by step
- Never ask for sensitive personal information
"""

# --------------------------------------------------
# STREAMLIT UI
# --------------------------------------------------
st.title("🤖 Conversational Chatbot")
st.caption("Powered by AI | Education")

# Initialize chat history with system prompt
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# Display chat history (hide system prompt)
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# User input
prompt = st.chat_input("Type your message...")

if prompt:
    # Add user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Call OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages
    )

    reply = response.choices[0].message.content

    # Add assistant message
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

    with st.chat_message("assistant"):
        st.markdown(reply)

    # Trim history (keep system prompt)
    MAX_MESSAGES = 20
    st.session_state.messages = (
        [st.session_state.messages[0]] +
        st.session_state.messages[-MAX_MESSAGES:]
    )
