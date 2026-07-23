import os
from dotenv import load_dotenv
from google import genai
from vector_store import search
import streamlit as st

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        api_key = None

client = genai.Client(api_key=api_key)

DISCLAIMER = "\n\n⚠️ This chatbot is for educational purposes only and is not a substitute for professional medical advice."


def build_prompt(question, retrieved_chunks):
    context_text = "\n\n".join(
        [f"[{c['source_file']} - Page {c['page_number']}]: {c['text']}" for c in retrieved_chunks]
    )

    prompt = f"""You are a medical information assistant. Answer the user's question using ONLY the context below, which comes from uploaded medical documents.

Rules:
- Only describe symptoms, disease information, or facts explicitly stated in the context.
- Do NOT diagnose the user or tell them whether they have a disease.
- Do NOT suggest treatment unless it is explicitly present in the context.
- If the context does not contain the answer, say clearly: "I don't have this information in the uploaded documents."
- Keep the answer concise and clear.

Context:
{context_text}

Question: {question}

Answer:"""
    return prompt


def ask_question(question, top_k=3):
    retrieved_chunks = search(question, top_k=top_k)
    prompt = build_prompt(question, retrieved_chunks)

    import time
    max_retries = 3
    answer = None

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompt
            )
            answer = response.text
            break
        except Exception:
            if attempt < max_retries - 1:
                time.sleep(3)
            else:
                answer = "Sorry, the AI service is temporarily busy. Please try asking again in a moment."

    sources_used = sorted(set(f"{c['source_file']} (page {c['page_number']})" for c in retrieved_chunks))
    citation_text = "\n\n📚 Sources: " + ", ".join(sources_used)

    return answer + citation_text + DISCLAIMER


if __name__ == "__main__":
    question = "What is dengue?"
    result = ask_question(question)
    print(result)
