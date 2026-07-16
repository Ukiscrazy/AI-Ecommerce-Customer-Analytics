import psycopg2
import pandas as pd

conn = psycopg2.connect(
    host="localhost",
    database="ai_ecommerce_analytics",
    user="postgres",
    password="you.mezh63@",
    port="5432"
)

query = """
SELECT
c.customer_id,
c.first_name,
c.last_name,
ROUND(SUM(oi.total_amount),2) AS total_spent
FROM customers c
JOIN orders o
ON c.customer_id=o.customer_id
JOIN order_items oi
ON o.order_id=oi.order_id
GROUP BY
c.customer_id,
c.first_name,
c.last_name
ORDER BY total_spent DESC
LIMIT 10;
"""

df=pd.read_sql(query,conn)

print(df)

conn.close()