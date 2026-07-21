import streamlit as st
import os
from pdf_loader import load_pdf
from vector_store import add_pdf_to_index
from qa_chain import ask_question

st.set_page_config(page_title="Medical AI Assistant", page_icon="🩺")
st.title("🩺 Medical AI Assistant")
st.caption("Ask about disease symptoms based on your uploaded medical documents.")

# --- Session state setup (persists across reruns) ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "index_built" not in st.session_state:
    st.session_state.index_built = False

# --- PDF Upload Section ---
st.subheader("📄 Upload a Medical PDF")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    save_path = os.path.join("data/pdfs", uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    if st.button("Add this PDF to Knowledge Base"):
        with st.spinner("Reading and indexing PDF... this may take a moment"):
            add_pdf_to_index(save_path)
        st.session_state.index_built = True
        st.success(f"Added: {uploaded_file.name}")

# --- Chat Section ---
st.subheader("💬 Ask a Question")

if not st.session_state.index_built:
    st.info("Upload a PDF and click 'Build Knowledge Base' before asking questions.")

# Display past conversation
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)

# Chat input box
user_question = st.chat_input("Ask about symptoms, e.g. 'What are the symptoms of dengue?'")

if user_question:
    st.session_state.chat_history.append(("user", user_question))
    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):
        with st.spinner("Searching documents..."):
            answer = ask_question(user_question)
        st.markdown(answer)

    st.session_state.chat_history.append(("assistant", answer))