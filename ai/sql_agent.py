from ai.chatbot import ask_groq

SCHEMA = """
Database: ai_ecommerce_analytics

Tables:

customers(
    customer_id,
    first_name,
    last_name,
    email,
    city,
    state
)

orders(
    order_id,
    customer_id,
    order_date
)

order_items(
    item_id,
    order_id,
    product_id,
    quantity,
    unit_price,
    discount_percent,
    total_amount
)

products(
    product_id,
    product_name,
    category
)

Relationships:

customers.customer_id = orders.customer_id

orders.order_id = order_items.order_id

products.product_id = order_items.product_id

Business Rules:

1. Revenue MUST ALWAYS use:
   SUM(order_items.total_amount)

2. Customer spending MUST ALWAYS use:
   SUM(order_items.total_amount)

3. Best selling products use:
   SUM(order_items.quantity)

4. Monthly sales:
   DATE_TRUNC('month', orders.order_date)

5. Never use a column named:
   price

6. Never invent columns.

7. Use only the columns listed above.
"""


def generate_sql(question):

    prompt = f"""
You are an expert PostgreSQL SQL developer.

Convert the user's business question into a PostgreSQL query.

Rules:

1. Return ONLY SQL.
2. No explanation.
3. No markdown.
4. No ```sql.
5. Use PostgreSQL syntax only.
6. Never invent tables.
7. Never invent columns.
8. Use only the schema provided.
9. Revenue = SUM(order_items.total_amount)
10. Customer Spending = SUM(order_items.total_amount)
11. Best Selling Products = SUM(order_items.quantity)
12. Monthly reports use DATE_TRUNC('month', orders.order_date)
13. Always generate executable SQL.
14. If joining tables, use the relationships provided.

Database Schema:

{SCHEMA}

User Question:
{question}
"""

    sql = ask_groq(prompt)

    if sql is None:
        return None

    sql = (
        sql.replace("```sql", "")
        .replace("```", "")
        .strip()
    )

    return sql