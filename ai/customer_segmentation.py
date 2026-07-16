import pandas as pd

from dashboard.database import run_query


def segment(score):

    r = int(score[0])
    f = int(score[1])
    m = int(score[2])

    if r >= 4 and f >= 4 and m >= 4:
        return "🏆 Champions"

    elif r >= 3 and f >= 4:
        return "💎 Loyal Customers"

    elif r >= 4 and f <= 3:
        return "🌱 Potential Loyalists"

    elif r <= 2 and f >= 3:
        return "⚠️ At Risk"

    else:
        return "❌ Lost Customers"


def get_rfm():

    query = """
    SELECT
        c.customer_id,
        c.first_name || ' ' || c.last_name AS customer_name,
        MAX(o.order_date) AS last_order,
        COUNT(DISTINCT o.order_id) AS frequency,
        SUM(oi.total_amount) AS monetary

    FROM customers c

    JOIN orders o
        ON c.customer_id = o.customer_id

    JOIN order_items oi
        ON o.order_id = oi.order_id

    GROUP BY
        c.customer_id,
        customer_name
    """

    df = run_query(query)

    today = pd.Timestamp.today()

    df["last_order"] = pd.to_datetime(df["last_order"])

    df["recency"] = (today - df["last_order"]).dt.days

    df["R"] = pd.qcut(df["recency"], 5, labels=[5, 4, 3, 2, 1])
    df["F"] = pd.qcut(df["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
    df["M"] = pd.qcut(df["monetary"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])

    df["RFM Score"] = (
        df["R"].astype(str)
        + df["F"].astype(str)
        + df["M"].astype(str)
    )

    df["Segment"] = df["RFM Score"].apply(segment)

    return df