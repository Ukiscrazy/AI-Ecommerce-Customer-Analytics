import psycopg2
import pandas as pd

conn=psycopg2.connect(
host="localhost",
database="ai_ecommerce_analytics",
user="postgres",
password="you.mezh63@",
port="5432"
)

query="""
SELECT
p.product_name,
SUM(oi.quantity) AS quantity_sold,
ROUND(SUM(oi.total_amount),2) AS revenue
FROM products p
JOIN order_items oi
ON p.product_id=oi.product_id
GROUP BY p.product_name
ORDER BY revenue DESC
LIMIT 10;
"""

df=pd.read_sql(query,conn)

print(df)

conn.close()