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
├── data/pdfs/ # Uploaded PDFs stored here
├── vectorstore/faiss_index/ # FAISS index + metadata (auto-generated)
├── pdf_loader.py # Reads PDFs, splits into chunks, tracks page numbers
├── embeddings.py # Converts text chunks into vectors
├── vector_store.py # Builds/loads FAISS index, similarity search
├── qa_chain.py # RAG logic: retrieve + Gemini + citations
├── app.py # Streamlit UI
├── requirements.txt
└── .env # API key (not committed)


## Setup Instructions

1. Clone this repository:

git clone https://github.com/aayushigupta004/medical-ai-assistant.git
cd medical-ai-assistant
2. Create and activate a virtual environment (Python 3.11 recommended):
python -m venv venv
venv\Scripts\activate # Windows
source venv/bin/activate # Mac/Linux


3. Install dependencies:

pip install -r requirements.txt


4. Create a `.env` file in the project root with your Gemini API key:

GEMINI_API_KEY=your_key_here

   Get a free key at [aistudio.google.com](https://aistudio.google.com).

5. Run the app:

streamlit run app.py
6. Open `http://localhost:8501` in your browser, upload a medical PDF, click "Add this PDF to Knowledge Base", and start asking questions.

## Disclaimer
This chatbot is for educational purposes only and is not a substitute for professional medical advice.

## Limitations
- Answers are only as good as the uploaded documents' content and text quality
- Not designed or intended for medical diagnosis
