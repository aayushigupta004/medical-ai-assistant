import streamlit as st
import os
from pdf_loader import load_pdf
from vector_store import add_pdf_to_index
from qa_chain import ask_question

st.set_page_config(
    page_title="Medical AI Assistant",
    page_icon="🩺",
    layout="wide"
)

# ---------- Custom CSS for a ChatGPT-like landing look ----------
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .stApp {
        background-color: #0f0f0f;
    }

    .main .block-container {
        max-width: 720px;
        padding-top: 4rem;
        padding-bottom: 6rem;
    }

    /* Centered greeting text, ChatGPT style */
    .greeting {
        text-align: center;
        font-size: 2rem;
        font-weight: 600;
        color: #ececec;
        margin-top: 8vh;
        margin-bottom: 2rem;
    }

    .subgreeting {
        text-align: center;
        color: #9b9b9b;
        font-size: 0.95rem;
        margin-bottom: 2.5rem;
    }

    /* Pill-shaped chat input, like ChatGPT's "Ask anything" box */
    [data-testid="stChatInput"] {
        background-color: #1e1e1e;
        border-radius: 28px;
        border: 1px solid #333;
        padding: 0.3rem 0.5rem;
    }
    [data-testid="stChatInput"] textarea {
        color: #ececec !important;
    }

    /* Chat message bubbles */
    [data-testid="stChatMessage"] {
        background-color: transparent;
        padding: 1rem 0;
        border-bottom: 1px solid #222;
    }
    [data-testid="stChatMessage"] p {
        font-size: 0.95rem;
        line-height: 1.6;
        color: #ececec;
    }

    /* Upload expander styling */
    [data-testid="stExpander"] {
        background-color: #1a1a1a;
        border-radius: 14px;
        border: 1px solid #2a2a2a;
        margin-bottom: 1.5rem;
    }

    .stButton button {
        background-color: #2563eb;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 0.5rem 1.4rem;
        font-weight: 500;
    }
    .stButton button:hover {
        background-color: #1d4ed8;
    }

    .stAlert {
    border-radius: 10px;
}

.sidebar-footer {
    position: fixed;
    left: 15px;
    bottom: 15px;
    width: 240px;
    text-align: center;
    color: #9ca3af;
    font-size: 14px;
    border-top: 1px solid #333;
    padding-top: 12px;
    background-color: #0f0f0f;
}
</style>
""", unsafe_allow_html=True)

# --- Session state setup ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "index_built" not in st.session_state:
    st.session_state.index_built = False

# --- PDF Upload Section (collapsible) ---
with st.sidebar:
    st.title("📄 Upload PDF")

    uploaded_file = st.file_uploader(
        "Choose a Medical PDF",
        type="pdf"
    )

    if uploaded_file is not None:
        save_path = os.path.join("data/pdfs", uploaded_file.name)

        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        if st.button("Add PDF"):
            with st.spinner("Reading and indexing PDF..."):
                add_pdf_to_index(save_path)
            st.session_state.index_built = True
            st.markdown("""
    <div class="sidebar-footer">
        <b>🩺 Medical AI Assistant</b><br>
        Version 1.0.0<br><br>
        Developed by<br>
        <b>Ayushi Gupta</b>
    </div>
    """, unsafe_allow_html=True)

# --- ChatGPT-style greeting, shown only when chat is empty ---
if len(st.session_state.chat_history) == 0:
    st.markdown('<div class="greeting">🩺 Medical AI Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="subgreeting">Ask about disease symptoms based on your uploaded medical documents.</div>', unsafe_allow_html=True)

# --- Chat message display ---
for role, message in st.session_state.chat_history:
    avatar = "🧑" if role == "user" else "🩺"
    with st.chat_message(role, avatar=avatar):
        st.markdown(message)

# --- Chat input (fixed at bottom, pill-shaped) ---
user_question = st.chat_input("Ask about symptoms, e.g. 'What are the symptoms of dengue?'")

if user_question:
    st.session_state.chat_history.append(("user", user_question))
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_question)

    with st.chat_message("assistant", avatar="🩺"):
        with st.spinner("Searching documents..."):
            answer = ask_question(user_question)
        st.markdown(answer)

    st.session_state.chat_history.append(("assistant", answer))
