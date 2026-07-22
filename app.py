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

# ---------- Custom CSS for a ChatGPT/Gemini-like look ----------
st.markdown("""
<style>
    /* Hide default Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Overall page background */
    .stApp {
        background-color: #0f0f0f;
    }

    /* Center content like ChatGPT's column width */
    .main .block-container {
        max-width: 800px;
        padding-top: 2rem;
        padding-bottom: 6rem;
    }

    /* Title styling */
    h1 {
        font-size: 1.8rem !important;
        font-weight: 600 !important;
        color: #ececec !important;
    }

    /* Chat message bubbles */
    [data-testid="stChatMessage"] {
        background-color: transparent;
        padding: 1rem 0;
        border-bottom: 1px solid #2a2a2a;
    }

    /* User message text */
    [data-testid="stChatMessage"] p {
        font-size: 0.95rem;
        line-height: 1.6;
        color: #ececec;
    }

    /* Chat input box styling */
    [data-testid="stChatInput"] {
        background-color: #1e1e1e;
        border-radius: 12px;
        border: 1px solid #333;
    }

    /* Upload box styling */
    [data-testid="stFileUploader"] {
        background-color: #1a1a1a;
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid #2a2a2a;
    }

    /* Buttons */
    .stButton button {
        background-color: #2563eb;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1.2rem;
        font-weight: 500;
    }
    .stButton button:hover {
        background-color: #1d4ed8;
    }

    /* Success/info boxes */
    .stAlert {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("### 🩺 Medical AI Assistant")
st.caption("Ask about disease symptoms based on your uploaded medical documents.")

# --- Session state setup ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "index_built" not in st.session_state:
    st.session_state.index_built = False

# --- PDF Upload Section (collapsible so chat feels like the main focus) ---
with st.expander("📄 Upload a Medical PDF", expanded=not st.session_state.index_built):
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", label_visibility="collapsed")

    if uploaded_file is not None:
        save_path = os.path.join("data/pdfs", uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        if st.button("Add this PDF to Knowledge Base"):
            with st.spinner("Reading and indexing PDF... this may take a moment"):
                add_pdf_to_index(save_path)
            st.session_state.index_built = True
            st.success(f"Added: {uploaded_file.name}")

if not st.session_state.index_built:
    st.info("Upload a PDF above and click 'Add this PDF to Knowledge Base' to get started.")

# --- Chat message display ---
for role, message in st.session_state.chat_history:
    avatar = "🧑" if role == "user" else "🩺"
    with st.chat_message(role, avatar=avatar):
        st.markdown(message)

# --- Chat input (fixed at bottom, like ChatGPT) ---
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
