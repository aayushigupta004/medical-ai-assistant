# Medical AI Assistant (RAG Chatbot)

A Retrieval-Augmented Generation chatbot that answers disease/symptom questions strictly from uploaded medical PDFs (WHO guidelines, medical references), with page-level source citations and a disclaimer on every answer.

## Features
- Upload medical PDFs (WHO guidelines, hospital documents, medical books)
- Ask questions about disease symptoms
- Answers are generated only from the uploaded documents — no external medical claims
- Every answer includes the source document + page number
- Conversation history maintained during the session
- Medical disclaimer shown on every response

## Tech Stack
- Python 3.11
- Streamlit (UI)
- LangChain (text splitting)
- FAISS (vector similarity search)
- Sentence Transformers (`all-MiniLM-L6-v2`) for embeddings
- Google Gemini API (`gemini-3-flash-preview`) for answer generation
- pypdf for PDF text extraction

## Project Structure

- `data/pdfs/` — Uploaded PDFs stored here
- `vectorstore/faiss_index/` — FAISS index + metadata (auto-generated)
- `pdf_loader.py` — Reads PDFs, splits into chunks, tracks page numbers
- `embeddings.py` — Converts text chunks into vectors
- `vector_store.py` — Builds/loads FAISS index, similarity search
- `qa_chain.py` — RAG logic: retrieve + Gemini + citations
- `app.py` — Streamlit UI
- `requirements.txt` — Python dependencies
- `.env` — API key (not committed)

## Setup Instructions

1. Clone this repository:
