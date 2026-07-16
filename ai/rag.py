import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Build an absolute path to the PDF so this works no matter
# which directory the script is run from.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PDF_PATH = os.path.join(PROJECT_ROOT, "Business_Report.pdf")


def load_documents():

    if not os.path.exists(PDF_PATH):
        raise FileNotFoundError(
            f"PDF not found at expected path: {PDF_PATH}\n"
            f"Make sure 'Business_Report.pdf' exists at your project root."
        )

    loader = PyPDFLoader(PDF_PATH)

    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    return splitter.split_documents(docs)