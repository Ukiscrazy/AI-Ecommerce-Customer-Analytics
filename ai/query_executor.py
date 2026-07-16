import psycopg2
import pandas as pd


# ==========================
# PostgreSQL Connection
# ==========================
DB_CONFIG = {
    "host": "localhost",
    "database": "ai_ecommerce_analytics",
    "user": "postgres",
    "password": "you.mezh63@",
    "port": "5432"
}


def execute_sql(sql_query):
    """
    Executes SQL query and returns the result as a Pandas DataFrame.
    """

    try:
        conn = psycopg2.connect(**DB_CONFIG)

        df = pd.read_sql(sql_query, conn)

        conn.close()

        return df

    except Exception as e:
        print("\nDatabase Error:")
        print(e)
        return None