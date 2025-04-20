import streamlit as st
import requests

# === Streamlit Page Setup ===
st.set_page_config(page_title="Crack-the-python", page_icon="⚡", layout="centered")
st.title("⚡ Crack-py: Your Python Chat Assistant")

# === Groq API Setup (Key is directly in code) ===
GROQ_API_KEY = "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"  # Use your actual key here
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama-3.3-70b-versatile"  # You can also try: llama3-8b-8192, gemma-7b-it, etc.

# === Define Bad Words for 18+ Blocker ===
bad_words = ["adult", "18+", "explicit", "porn", "sex", "xxx"]  # Add more inappropriate words as needed

# === Check if Input Contains a Name Question ===
def is_name_question(input_text):
    return "your name" in input_text or "who are you" in input_text or "what's your name" in input_text

# === Check if Input Contains a Creator Question ===
def is_creator_question(input_text):
    return "creator" in input_text or "made you" in input_text or "who created you" in input_text

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
    lower_input = user_input.lower().strip()
    st.chat_message("user", avatar="🧑").markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # === 18+ BLOCKER ===
    if any(bad_word in lower_input for bad_word in bad_words):
        reply = "⚠️ This is not advisory. I'm calling 100 🚨. Stay tuned guys!"

    # === NAME Q&A ===
    elif is_name_question(lower_input):
        reply = (
            "Hey there! I'm Crack-head, but my friends call me Susru 🤖\n"
            "I'm your Python-focused chatbot with attitude and brains 💥\n"
            "I was born to crack problems, debug chaos, and vibe with coders 🧠\n"
            "I'm not just smart, I'm built to slay Python questions with style!\n"
            "So yeah, I’m here to be your coding companion.\n"
            "Ask me anything related to Python, and I’ll give it my all 🐍✨"
        )

    # === CREATOR Q&A ===
    elif is_creator_question(lower_input):
        reply = (
            "I was proudly created by TB-Solutions 💡\n"
            "The mind behind me is Tharun Bala — a true Python & AI enthusiast 🤓\n"
            "He crafted me using Groq API and Streamlit, fueled by caffeine ☕\n"
            "This bot isn't just a tool, it's a piece of heart and hustle 💻💙\n"
            "Tharun believes tech should be fun, fast, and friendly.\n"
        )

    else:
        # Prepare API call for normal chat
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
            else:
                reply = f"API Error {response.status_code}: {response.text}"

    # Show assistant's reply
    st.chat_message("assistant").markdown(reply)
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
