from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from app.utils.pdf_parser import extract_text_from_pdf
import os

# Initialize OpenAI API key
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def vectorize_and_store_pdf(
    file_path: str, index_path: str = "vector_store/faiss_index"
) -> FAISS:
    # Step 1: Extract text from the PDF
    text = extract_text_from_pdf(file_path)

    # Step 2: Initialize OpenAI embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    # Step 3: Create vector store (FAISS)
    vector_store = FAISS.from_texts([text], embeddings)

    # Step 4: Save the FAISS index to disk
    if not os.path.exists(index_path):
        os.makedirs(index_path)
    vector_store.save_local(index_path)

    return vector_store
