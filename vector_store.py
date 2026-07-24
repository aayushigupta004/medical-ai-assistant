import faiss
import numpy as np
import pickle
import os

from pdf_loader import load_pdf
from embeddings import get_embeddings

INDEX_PATH = "vectorstore/faiss_index/index.faiss"
METADATA_PATH = "vectorstore/faiss_index/metadata.pkl"


def add_pdf_to_index(pdf_path):
    """
    Loads a PDF, creates chunks, embeds them, and ADDS them to the
    existing FAISS index (or creates a new one if none exists yet).
    """
    filename = os.path.basename(pdf_path)
    chunks = load_pdf(pdf_path)

    for c in chunks:
        c["source_file"] = filename

    texts = [c["text"] for c in chunks]
    vectors = get_embeddings(texts)
    vectors = np.array(vectors).astype("float32")

    os.makedirs("vectorstore/faiss_index", exist_ok=True)

    if os.path.exists(INDEX_PATH) and os.path.exists(METADATA_PATH):
        index = faiss.read_index(INDEX_PATH)
        with open(METADATA_PATH, "rb") as f:
            existing_chunks = pickle.load(f)
    else:
        dimension = vectors.shape[1]
        index = faiss.IndexFlatL2(dimension)
        existing_chunks = []

    index.add(vectors)
    existing_chunks.extend(chunks)

    faiss.write_index(index, INDEX_PATH)
    with open(METADATA_PATH, "wb") as f:
        pickle.dump(existing_chunks, f)

    print(f"Added {len(chunks)} chunks from '{filename}'. Total chunks in index: {len(existing_chunks)}")


def load_index():
    index = faiss.read_index(INDEX_PATH)
    with open(METADATA_PATH, "rb") as f:
        chunks = pickle.load(f)
    return index, chunks


def search(query, top_k=3):
    index, chunks = load_index()

    query_vector = get_embeddings([query])
    query_vector = np.array(query_vector).astype("float32")

    distances, indices = index.search(query_vector, top_k)

    results = []
    for idx in indices[0]:
        results.append(chunks[idx])

    return results


if __name__ == "__main__":
    add_pdf_to_index("data/pdfs/test.pdf")
    results = search("What is dengue?", top_k=2)
    print("\n---- Search results ----")
    for r in results:
        print(f"{r['source_file']} - Page {r['page_number']}: {r['text']}")