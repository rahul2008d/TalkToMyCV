from langchain_community.document_loaders import PyPDFLoader, PyMuPDFLoader


def extract_text_from_pdf(file_path: str) -> str:
    # loader = PyPDFLoader("example_data/layout-parser-paper.pdf")
    loader = PyMuPDFLoader(file_path)
    pages = loader.load_and_split()
    return pages
