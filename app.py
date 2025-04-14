import streamlit as st
import requests

# === API Config ===
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"

# === Bad Words List ===
bad_words = [
    "sex", "nude", "naked", "porn", "hot girl", "hot boy", "boobs", "d*ck", "f*ck",
    "s*x", "horny", "xxx", "erotic", "18+", "adult", "nsfw"
]

# === Streamlit Setup ===
st.set_page_config(page_title="Crack-the-py", layout="wide", page_icon="🤖")

# === Session Chat History ===
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# === Custom CSS ===
st.markdown("""
    <style>
        body, .stApp {
            font-family: 'Segoe UI', sans-serif;
            background-color: #f0f2f6;
        }
        .stChatMessage .stTextArea, .stChatMessage .stTextInput {
            border-radius: 10px;
            padding: 10px;
        }
        .stMarkdown {
            font-size: 16px;
        }
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# === Header ===
st.title("Crack-the-py-ChatBot (Python Only 🐍)")
if st.button("🗑️ Clear Chat"):
    st.session_state.chat_history = []

# === Chat Input ===
user_input = st.chat_input("Ask Python questions here...")

# === Groq API Call ===
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
        return f"⚠️ API Error {response.status_code}"

# === Python Question Checker ===
def is_python_related(message):
    keywords = [
        "python", "pandas", "numpy", "tkinter", "django", "flask", "pyqt", "scikit",
        "matplotlib", "plotly", "streamlit", "code", "program", "script", "function",
        "class", "exception", "list", "tuple", "dict", "loop", "conditional", "variable"
    ]
    return any(word in message.lower() for word in keywords)
# === Handle User Input ===
if user_input:
    lower_input = user_input.lower().strip()

    st.chat_message("user", avatar="🧑").markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # === Check for bad content
    if any(bad_word in lower_input for bad_word in bad_words):
        reply = "⚠️ This is not advisory. I'm calling 100 🚔. Stay tuned guys!"

    # === Specific allowed Meta Q&A
    elif any(q in lower_input for q in ["your name", "what is your name", "who are you", "tell me your name"]):
        reply = (
            "Hey there! I'm Crack-head, but my friends call me Susru 🤖\n"
            "I'm your personal Python assistant built with some serious AI brainpower.\n"
            "I'm designed to answer your coding questions—especially Python ones—with style.\n"
            "Whether it's NumPy, Pandas, or Streamlit, I’ve got your back.\n"
            "I stay focused only on Python-related stuff to keep things sharp and clean.\n"
            "So let’s crack some code together, shall we? 💻🐍"
        )

    elif any(q in lower_input for q in ["who created you", "who made you", "developer", "who is your creator", "who built you"]):
        reply = (
            "I was proudly built by **TB-Solutions**, founded by the one and only Tharun Bala ⚡️\n"
            "He’s a young AI enthusiast and Python pro who’s passionate about making tech fun and useful.\n"
            "Crack-head (that’s me) was designed to focus on Python programming and help developers like you.\n"
            "This isn't just a bot—it's a project filled with love, code, and a dash of attitude 😎\n"
            "Tharun combined Groq's blazing fast API with clean Streamlit UI to bring me to life.\n"
            "You could say I'm part code, part chaos... and totally made to help you learn!"
        )

    # === Check if Python related
    elif not is_python_related(lower_input):
        reply = "⚠️ Sorry, I only answer Python or programming-related questions. Please ask something related to Python 🐍."

    # === Valid Python Q&A
    else:
        with st.spinner("Thinking..."):
            reply = get_groq_response(st.session_state.chat_history)

    st.chat_message("assistant", avatar="🤖").markdown(reply)
    st.session_state.chat_history.append({"role": "assistant", "content": reply})

# === Display Chat History ===
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.chat_message("user", avatar="🧑").write(msg["content"])
    else:
        st.chat_message("assistant", avatar="🤖").write(msg["content"])
