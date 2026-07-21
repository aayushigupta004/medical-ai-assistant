from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_pdf(file_path, chunk_size=500, chunk_overlap=50):
    """
    Reads a PDF, splits each page into smaller chunks,
    and returns a list of dicts:
    [{"page_number": 1, "text": "chunk text..."}, ...]
    """
    reader = PdfReader(file_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    chunks_data = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        page_number = i + 1

        if text and text.strip():
            page_chunks = splitter.split_text(text)
            for chunk in page_chunks:
                chunks_data.append({
                    "page_number": page_number,
                    "text": chunk
                })

    return chunks_data


if __name__ == "__main__":
    test_file = "data/pdfs/test.pdf"
    result = load_pdf(test_file)
    print(f"Total chunks created: {len(result)}")
    print("---- All chunks ----")
    for chunk in result:
        print(f"Page {chunk['page_number']}: {chunk['text']}")