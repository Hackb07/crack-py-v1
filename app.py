import streamlit as st
import requests
import json

# === CONFIG ===
GROQ_API_KEY = "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"  # Replace with your actual API key
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"

# === BANNED CONTENT CHECK ===
bad_words = [
    "sex", "nude", "naked", "porn", "hot girl", "hot boy", "boobs", "d*ck",
    "f*ck", "s*x", "horny", "xxx", "erotic", "18+", "adult", "nsfw"
]

# === PAGE CONFIG ===
st.set_page_config(page_title="Crack-head ChatBot", layout="wide", page_icon="🤖")

# === SESSION STATE ===
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# === CSS STYLE ===
st.markdown("""
    <style>
        .stApp {
            font-family: 'Segoe UI', sans-serif;
            background-color: #f4f6f9;
        }
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# === FUNCTIONS ===
def is_python_related(query):
    python_keywords = [
        "python", "numpy", "pandas", "dataframe", "list", "tuple", "dictionary",
        "set", "loop", "function", "lambda", "decorator", "class", "object",
        "machine learning", "AI", "data science", "streamlit", "flask", "api",
        "matplotlib", "seaborn", "pyplot", "csv", "json", "file handling"
    ]
    return any(kw in query.lower() for kw in python_keywords)

def is_name_question(text):
    return any(q in text for q in ["your name", "what is your name", "who are you", "tell me your name","name"])

def is_creator_question(text):
    return any(q in text for q in ["who created you", "who made you", "who is your creator", "developer", "built you","creator","author","Your god"])

def get_groq_response(messages):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7
    }
    response = requests.post(GROQ_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"⚠️ API Error: {response.status_code}"

# === UI HEADER ===
st.title("🤖 Crack-head  - Your coding Assistant ......... :)")
if st.button("🗑️ Clear Chat"):
    st.session_state.chat_history = []

# === USER INPUT ===
user_input = st.chat_input("Ask me something related to Python...")

# === CHAT HANDLER ===
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
            "So if I seem cool, give the credit to him 😎🔥"
        )

    # === PYTHON-ONLY FILTER ===
    elif not is_python_related(lower_input):
        reply = "⚠️ Sorry, I only answer Python-related or programming-related questions. Please keep it in the dev zone 🐍💬"

    # === PYTHON ANSWER FROM GROQ ===
    else:
        with st.spinner("Thinking..."):
            reply = get_groq_response(st.session_state.chat_history)

    # === DISPLAY BOT RESPONSE ===
    st.chat_message("assistant", avatar="🤖").markdown(reply)
    st.session_state.chat_history.append({"role": "assistant", "content": reply})

# === DISPLAY PAST CHAT HISTORY ===
for msg in st.session_state.chat_history:
    role = msg["role"]
    avatar = "🧑" if role == "user" else "🤖"
    st.chat_message(role, avatar=avatar).markdown(msg["content"])
