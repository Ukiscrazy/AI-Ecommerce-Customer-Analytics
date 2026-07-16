import os
import streamlit as st
import psycopg2
import pandas as pd
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

# Load .env from the project root (used for local development)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))


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


DB_HOST = get_secret("DB_HOST")
DB_PORT = get_secret("DB_PORT")
DB_USER = get_secret("DB_USER")
DB_PASSWORD = get_secret("DB_PASSWORD")
DB_NAME = get_secret("DB_NAME")

# Fallback local config, used only if cloud DB secrets are not set at all
LOCAL_DB_CONFIG = {
    "host": "localhost",
    "database": "ai_ecommerce_analytics",
    "user": "postgres",
    "password": "you.mezh63@",
    "port": "5432"
}


def get_connection():

    if DB_HOST and DB_USER and DB_PASSWORD:
        return psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME
        )

    return psycopg2.connect(
        host=LOCAL_DB_CONFIG["host"],
        database=LOCAL_DB_CONFIG["database"],
        user=LOCAL_DB_CONFIG["user"],
        password=LOCAL_DB_CONFIG["password"],
        port=LOCAL_DB_CONFIG["port"]
    )


def run_query(query, params=None):

    conn = get_connection()

    try:

        df = pd.read_sql(
            query,
            conn,
            params=params
        )

        return df

    finally:

        conn.close()


def execute_query(query, params=None):

    conn = get_connection()

    cur = conn.cursor(cursor_factory=RealDictCursor)

    try:

        cur.execute(query, params)

        conn.commit()

        try:
            rows = cur.fetchall()
            return pd.DataFrame(rows)
        except Exception:
            return pd.DataFrame()

    finally:

        cur.close()
        conn.close()


def test_connection():

    try:

        conn = get_connection()

        conn.close()

        return True

    except Exception:

        return False
