import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

conn = psycopg2.connect(
    host="localhost",
    database="ai_ecommerce_analytics",
    user="postgres",
    password="you.mezh63@",
    port="5432"
)

query = """
SELECT
    category,
    ROUND(SUM(oi.total_amount),2) AS revenue
FROM order_items oi
JOIN products p
ON oi.product_id = p.product_id
GROUP BY category
ORDER BY revenue DESC;
"""

df = pd.read_sql(query, conn)

print(df)

plt.figure(figsize=(10,6))

plt.bar(df["category"], df["revenue"])

plt.title("Revenue by Category")
plt.xlabel("Category")
plt.ylabel("Revenue")

plt.tight_layout()

plt.show()

conn.close()