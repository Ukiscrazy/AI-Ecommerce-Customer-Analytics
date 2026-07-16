import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        database="ai_ecommerce_analytics",
        user="postgres",
        password="you.mezh63@",
        port="5432"
    )

    print("✅ Connected to PostgreSQL Successfully!")

    conn.close()

except Exception as e:
    print("Connection Failed!")
    print(e)