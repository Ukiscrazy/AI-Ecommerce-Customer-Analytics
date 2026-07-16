from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from ai.rag import load_documents

def create_vector_db():

    docs = load_documents()

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = FAISS.from_documents(docs, embeddings)

    db.save_local("vector_db")

    return db