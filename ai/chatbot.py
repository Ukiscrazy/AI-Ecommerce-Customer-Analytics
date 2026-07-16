import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))


def get_secret(key):
    value = os.getenv(key)
    if value:
        return value
    try:
        return st.secrets[key]
    except Exception:
        return None


API_KEY = get_secret("GROQ_API_KEY")

if not API_KEY:
    raise ValueError("GROQ_API_KEY not found. Add it to .env locally or Streamlit Cloud secrets.")

client = Groq(api_key=API_KEY)

DEFAULT_SQL_SYSTEM_PROMPT = (
    "You are an expert PostgreSQL SQL developer. "
    "Convert English questions into PostgreSQL SQL. "
    "Return ONLY SQL without explanations, markdown or code blocks."
)


def ask_groq(prompt, system_prompt=DEFAULT_SQL_SYSTEM_PROMPT):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
            max_tokens=1024,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"\nGroq Error:\n{e}")
        return None