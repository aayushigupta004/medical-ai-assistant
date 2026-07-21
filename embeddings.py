from sentence_transformers import SentenceTransformer

# Load the embedding model once (this happens the first time you run this file --
# it may download the model, ~80MB, the first time only)
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embeddings(text_chunks):
    """
    Takes a list of text strings and returns a list of embedding vectors.
    Each vector is a list of floating point numbers.
    """
    embeddings = model.encode(text_chunks, show_progress_bar=True)
    return embeddings


if __name__ == "__main__":
    sample_texts = [
        "Dengue is a viral infection spread by mosquitoes.",
        "Common symptoms include high fever and headache.",
        "The weather today is sunny and warm."
    ]

    vectors = get_embeddings(sample_texts)

    print(f"Number of texts: {len(sample_texts)}")
    print(f"Vector shape: {vectors.shape}")
    print("First 5 numbers of first vector:", vectors[0][:5])