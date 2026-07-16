import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

conn=psycopg2.connect(
host="localhost",
database="ai_ecommerce_analytics",
user="postgres",
password="you.mezh63@",
port="5432"
)

query="""
SELECT
DATE_TRUNC('month',order_date) AS month,
COUNT(order_id) AS orders
FROM orders
GROUP BY month
ORDER BY month;
"""

df=pd.read_sql(query,conn)

print(df)

plt.figure(figsize=(10,5))
plt.plot(df["month"],df["orders"],marker="o")
plt.title("Monthly Orders")
plt.xlabel("Month")
plt.ylabel("Orders")
plt.grid(True)
plt.tight_layout()
plt.show()

conn.close()