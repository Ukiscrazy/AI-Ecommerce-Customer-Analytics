import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# =====================================================
# LOAD ENV
# =====================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

load_dotenv(
    os.path.join(PROJECT_ROOT, ".env")
)


def get_secret(key):
    """
    Reads a config value from, in order:
    1. Environment variables (populated locally via .env)
    2. Streamlit Cloud's st.secrets (used in deployment)
    Returns None if not found anywhere.
    """
    value = os.getenv(key)
    if value:
        return value
    try:
        return st.secrets[key]
    except Exception:
        return None


API_KEY = get_secret("GROQ_API_KEY")

if not API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found. Add it to .env locally or Streamlit Cloud secrets."
    )

client = Groq(api_key=API_KEY)

# =====================================================
# LOAD VECTOR DB
# =====================================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.load_local(
    os.path.join(PROJECT_ROOT, "vector_db"),
    embeddings,
    allow_dangerous_deserialization=True
)

# =====================================================
# PDF CHAT
# =====================================================

def ask_pdf(question):

    docs = db.similarity_search(
        question,
        k=4
    )

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    prompt = f"""
You are a helpful business analyst.

Answer ONLY using the provided document context.

Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=1024
    )

    return response.choices[0].message.content