import streamlit as st
import requests

# === Streamlit Page Setup ===
st.set_page_config(page_title="Crack-the-python", page_icon="⚡", layout="centered")
st.title("⚡ Crack-py: Your Python Chat Assistant")

# === Groq API Setup (Key is directly in code) ===
GROQ_API_KEY = "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"  # Use your actual key here
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama-3.3-70b-versatile"  # You can also try: llama3-8b-8192, gemma-7b-it, etc.

# === Session State for Chat ===
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# === Clear Chat Button ===
if st.button("🧹 Clear Chat"):
    st.session_state.chat_history = []
    st.success("Chat history cleared.")

# === Display Chat History ===
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# === Chat Input ===
user_input = st.chat_input("Ask me anything about Python, ML, or life...")

if user_input:
    # Show user's message
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Prepare API call
    with st.spinner("🤖 Thinking..."):
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": MODEL_NAME,
            "messages": st.session_state.chat_history,
            "temperature": 0.7
        }

        response = requests.post(GROQ_API_URL, headers=headers, json=data)

        if response.status_code == 200:
            reply = response.json()["choices"][0]["message"]["content"]
            st.chat_message("assistant").markdown(reply)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
        else:
            st.error(f"API Error {response.status_code}: {response.text}")
