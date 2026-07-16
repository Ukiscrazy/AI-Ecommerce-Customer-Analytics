import sys
import os
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.insert(0, PROJECT_ROOT)

from ai.email_report import send_report
from io import BytesIO
from ai.customer_segmentation import get_rfm
import pandas as pd
from ai.rag_chat import ask_pdf
from ai.recommendation_engine import generate_recommendations
import plotly.graph_objects as go
from ai.revenue_forecast import forecast_revenue
import streamlit as st
import plotly.express as px
from ai.sales_forecast import forecast_sales
from ai.report_generator import generate_pdf_report
from ai.business_summary import generate_executive_summary
from database import run_query, test_connection
from ai_chatbot import ai_chatbot
# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="AI E-Commerce Analytics",
    page_icon="🛒",
    layout="wide"
)
# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

.main{
    background:#0E1117;
}

div[data-testid="metric-container"]{
    background:#1f2937;
    border:1px solid #374151;
    border-radius:12px;
    padding:18px;
    box-shadow:0px 4px 12px rgba(0,0,0,.25);
}

h1,h2,h3{
    color:white;
}

section[data-testid="stSidebar"]{
    background:#111827;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# DATABASE CHECK
# ==========================================================

if not test_connection():
    st.error("❌ Unable to connect to PostgreSQL database.")
    st.stop()

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("🛒 AI Analytics")

page = st.sidebar.radio(
    "Navigation",
    [
        "📊 Dashboard",
        "🤖 AI Assistant",
        "📚 RAG Chat",
        "👥 Customer Segmentation"
    ]
)
st.sidebar.markdown("---")

st.sidebar.success("Database Connected")
st.sidebar.markdown("---")

st.sidebar.markdown("---")
st.sidebar.subheader("📌 Filters")
st.sidebar.markdown("---")
st.sidebar.subheader("📅 Date Filter")

min_date = run_query("""
SELECT MIN(order_date) AS min_date
FROM orders;
""").iloc[0]["min_date"]

max_date = run_query("""
SELECT MAX(order_date) AS max_date
FROM orders;
""").iloc[0]["max_date"]

start_date, end_date = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)
categories = run_query("""
SELECT DISTINCT category
FROM products
ORDER BY category;
""")

category = st.sidebar.selectbox(
    "Category",
    ["All"] + categories["category"].tolist()
)

# ==========================================================
# AI PAGE
# ==========================================================

if page == "🤖 AI Assistant":

    ai_chatbot()

    st.stop()
elif page == "📚 RAG Chat":

    st.title("📚 Chat with Business Documents")

    question = st.text_input(
        "Ask anything about the uploaded PDF"
    )

    if st.button("Ask PDF"):
        answer = ask_pdf(question)
        st.success(answer)

    st.stop()
elif page == "📚 RAG Chat":

    st.title("📚 Chat with Business Documents")

    question = st.text_input(
        "Ask anything about the uploaded PDF"
    )

    if st.button("Ask PDF"):
        answer = ask_pdf(question)
        st.success(answer)

    st.stop()

# ==========================================================
# CUSTOMER SEGMENTATION
# ==========================================================

elif page == "👥 Customer Segmentation":

    st.title("👥 Customer Segmentation (RFM Analysis)")

    rfm_df = get_rfm()

    segment_counts = (
        rfm_df["Segment"]
        .value_counts()
        .reset_index()
    )

    segment_counts.columns = [
        "Segment",
        "Customers"
    ]

    fig = px.pie(
        segment_counts,
        names="Segment",
        values="Customers",
        title="Customer Segment Distribution"
    )

    st.plotly_chart(
    fig,
    use_container_width=True
)

    st.subheader("Segment Summary")
    st.dataframe(
    segment_counts,
    use_container_width=True
)
    st.subheader("Top 10 Customers")

    top_customers = (
        rfm_df
        .sort_values("monetary", ascending=False)
        .head(10)
    )

    st.dataframe(
    top_customers[
        [
            "customer_name",
            "frequency",
            "monetary",
            "Segment"
        ]
    ],
    use_container_width=True
)
    st.stop()
# ==========================================================
# DASHBOARD
# ==========================================================

st.title("🛒 AI E-Commerce Customer Analytics Dashboard")

st.markdown("---")

# ==========================================================
# CATEGORY-AWARE QUERIES
# ==========================================================

customers = run_query("""
SELECT COUNT(*) AS total
FROM customers;
""")
if category == "All":

    orders_query = f"""
    SELECT
        DATE_TRUNC('month', order_date) AS month,
        COUNT(*) AS orders
    FROM orders
    WHERE order_date BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY DATE_TRUNC('month', order_date)
    ORDER BY month;
    """

else:

    orders_query = f"""
    SELECT
        DATE_TRUNC('month', o.order_date) AS month,
        COUNT(*) AS orders
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    JOIN products p
        ON oi.product_id = p.product_id
    WHERE p.category = '{category}'
      AND o.order_date BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY DATE_TRUNC('month', o.order_date)
    ORDER BY month;
    """

products = run_query("""
SELECT COUNT(*) AS total
FROM products;
""")

if category == "All":

    revenue = run_query(f"""
    SELECT ROUND(SUM(oi.total_amount),2) AS total
    FROM order_items oi
    JOIN orders o
        ON oi.order_id = o.order_id
    JOIN products p
        ON oi.product_id = p.product_id
    WHERE o.order_date BETWEEN '{start_date}' AND '{end_date}';
    """)

    category_query = f"""
    SELECT
        p.category,
        ROUND(SUM(oi.total_amount),2) AS revenue
    FROM order_items oi
    JOIN orders o
        ON oi.order_id = o.order_id
    JOIN products p
        ON oi.product_id = p.product_id
    WHERE o.order_date BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY p.category
    ORDER BY revenue DESC;
    """

    orders_query = f"""
    SELECT
        DATE_TRUNC('month', o.order_date) AS month,
        COUNT(*) AS orders
    FROM orders o
    WHERE o.order_date BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY DATE_TRUNC('month', o.order_date)
    ORDER BY month;
    """

    top_customer_query = f"""
    SELECT
        c.customer_id,
        c.first_name || ' ' || c.last_name AS customer_name,
        ROUND(SUM(oi.total_amount),2) AS spending
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    JOIN order_items oi
        ON o.order_id = oi.order_id
    JOIN products p
        ON oi.product_id = p.product_id
    WHERE o.order_date BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY
        c.customer_id,
        c.first_name,
        c.last_name
    ORDER BY spending DESC
    LIMIT 10;
    """

else:

    revenue = run_query(f"""
    SELECT ROUND(SUM(oi.total_amount),2) AS total
    FROM order_items oi
    JOIN orders o
        ON oi.order_id = o.order_id
    JOIN products p
        ON oi.product_id = p.product_id
    WHERE p.category = '{category}'
      AND o.order_date BETWEEN '{start_date}' AND '{end_date}';
    """)

    category_query = f"""
    SELECT
        p.category,
        ROUND(SUM(oi.total_amount),2) AS revenue
    FROM order_items oi
    JOIN orders o
        ON oi.order_id = o.order_id
    JOIN products p
        ON oi.product_id = p.product_id
    WHERE p.category = '{category}'
      AND o.order_date BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY p.category
    ORDER BY revenue DESC;
    """

    orders_query = f"""
    SELECT
        DATE_TRUNC('month', o.order_date) AS month,
        COUNT(*) AS orders
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    JOIN products p
        ON oi.product_id = p.product_id
    WHERE p.category = '{category}'
      AND o.order_date BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY DATE_TRUNC('month', o.order_date)
    ORDER BY month;
    """

    top_customer_query = f"""
    SELECT
        c.customer_id,
        c.first_name || ' ' || c.last_name AS customer_name,
        ROUND(SUM(oi.total_amount),2) AS spending
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    JOIN order_items oi
        ON o.order_id = oi.order_id
    JOIN products p
        ON oi.product_id = p.product_id
    WHERE p.category = '{category}'
      AND o.order_date BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY
        c.customer_id,
        c.first_name,
        c.last_name
    ORDER BY spending DESC
    LIMIT 10;
    """

category_df = run_query(category_query)
orders_df = run_query(orders_query)
top_customers = run_query(top_customer_query)
# ==========================================================
# KPI CARDS
# ==========================================================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "👥 Customers",
    f"{int(customers.iloc[0]['total']):,}"
)

c2.metric(
    "📦 Orders",
    f"{int(orders_df['orders'].sum()):,}"
)

c3.metric(
    "🛍 Products",
    f"{int(products.iloc[0]['total']):,}"
)

c4.metric(
    "💰 Revenue",
    f"₹ {float(revenue.iloc[0]['total']):,.2f}"
)

st.markdown("---")

k1, k2, k3 = st.columns(3)

avg_order = run_query("""
SELECT ROUND(AVG(total_amount),2) AS avg_order
FROM order_items;
""")

best_product = run_query("""
SELECT
p.product_name,
SUM(oi.quantity) AS qty
FROM order_items oi
JOIN products p
ON oi.product_id = p.product_id
GROUP BY p.product_name
ORDER BY qty DESC
LIMIT 1;
""")

total_orders = run_query("""
SELECT COUNT(*) AS total_orders
FROM orders;
""")

k1.metric(
    "💳 Average Order Value",
    f"₹ {float(avg_order.iloc[0]['avg_order']):,.2f}"
)

k2.metric(
    "🛒 Best Selling Product",
    best_product.iloc[0]["product_name"]
)

k3.metric(
    "📦 Total Orders",
    int(total_orders.iloc[0]["total_orders"])
)

# ==========================================================
# REVENUE BY CATEGORY
# ==========================================================

fig1 = px.bar(
    category_df,
    x="category",
    y="revenue",
    text="revenue",
    color="revenue",
    template="plotly_dark",
    title="Revenue by Category"
)

fig1.update_layout(
    coloraxis_showscale=False,
    xaxis_title="Category",
    yaxis_title="Revenue"
)

# ==========================================================
# MONTHLY ORDERS
# ==========================================================

fig2 = px.line(
    orders_df,
    x="month",
    y="orders",
    markers=True,
    template="plotly_dark",
    title="Monthly Orders"
)

fig2.update_layout(
    xaxis_title="Month",
    yaxis_title="Orders"
)

# ==========================================================
# REVENUE DISTRIBUTION
# ==========================================================

fig3 = px.pie(
    category_df,
    names="category",
    values="revenue",
    template="plotly_dark",
    title="Revenue Distribution"
)

# ==========================================================
# CHARTS
# ==========================================================

left, right = st.columns(2)

with left:
    st.plotly_chart(
        fig1,
        use_container_width=True
    )

with right:
    st.plotly_chart(
        fig2,
        use_container_width=True
    )

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.markdown("---")

# ==========================================================
# TOP CUSTOMERS
# ==========================================================

st.subheader("🏆 Top 10 Customers")

st.dataframe(
    top_customers,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# ==========================================================
# BUSINESS SUMMARY
# ==========================================================

summary1, summary2 = st.columns(2)

with summary1:

    highest_category = category_df.iloc[0]["category"]
    highest_revenue = category_df.iloc[0]["revenue"]

    st.success(
        f"🏆 Highest Revenue Category: **{highest_category}**\n\n"
        f"Revenue: ₹ {highest_revenue:,.2f}"
    )

with summary2:

    top_customer = top_customers.iloc[0]["customer_name"]
    top_spending = top_customers.iloc[0]["spending"]

    st.info(
        f"👤 Top Customer: **{top_customer}**\n\n"
        f"Spent: ₹ {top_spending:,.2f}"
    )

st.markdown("---")
# ==========================================================
# CUSTOMER SEGMENTATION (RFM)
# ==========================================================

st.subheader("👥 Customer Segmentation (RFM)")

rfm_df = get_rfm()

st.dataframe(
    rfm_df[
        [
            "customer_name",
            "Segment",
            "recency",
            "frequency",
            "monetary",
            "RFM Score",
        ]
    ],
    use_container_width=True,
    hide_index=True,
)
st.subheader("📊 Customer Segments")

segment_count = (
    rfm_df["Segment"]
    .value_counts()
    .reset_index()
)

segment_count.columns = ["Segment", "Customers"]

fig_segment = px.pie(
    segment_count,
    names="Segment",
    values="Customers",
    title="Customer Segmentation",
    template="plotly_dark"
)

st.plotly_chart(
    fig_segment,
    use_container_width=True
)
st.subheader("📌 Segment Summary")

c1, c2, c3 = st.columns(3)

champions = (rfm_df["Segment"] == "🏆 Champions").sum()
loyal = (rfm_df["Segment"] == "💎 Loyal Customers").sum()
atrisk = (rfm_df["Segment"] == "⚠️ At Risk").sum()

c1.metric("🏆 Champions", champions)
c2.metric("💎 Loyal", loyal)
c3.metric("⚠️ At Risk", atrisk)
# ==========================================================
# TOP PRODUCTS
# ==========================================================

st.subheader("🏆 Top 10 Products")

top_products = run_query("""
SELECT
    p.product_name,
    SUM(oi.quantity) AS units_sold,
    ROUND(SUM(oi.total_amount),2) AS revenue
FROM order_items oi
JOIN products p
ON oi.product_id = p.product_id
GROUP BY p.product_name
ORDER BY revenue DESC
LIMIT 10;
""")

st.dataframe(
    top_products,
    use_container_width=True,
    hide_index=True
)

fig_products = px.bar(
    top_products,
    x="product_name",
    y="revenue",
    color="revenue",
    text="revenue",
    template="plotly_dark",
    title="Top 10 Products by Revenue"
)

fig_products.update_layout(
    xaxis_title="Product",
    yaxis_title="Revenue"
)

st.plotly_chart(
    fig_products,
    use_container_width=True
)
# ==========================================================
# TOP CITIES
# ==========================================================

st.subheader("🏙 Top 10 Cities")

top_cities = run_query("""
SELECT
    c.city,
    ROUND(SUM(oi.total_amount),2) AS revenue
FROM customers c
JOIN orders o
ON c.customer_id = o.customer_id
JOIN order_items oi
ON o.order_id = oi.order_id
GROUP BY c.city
ORDER BY revenue DESC
LIMIT 10;
""")

st.dataframe(
    top_cities,
    use_container_width=True,
    hide_index=True
)

fig_city = px.bar(
    top_cities,
    x="city",
    y="revenue",
    color="revenue",
    text="revenue",
    template="plotly_dark",
    title="Top Cities by Revenue"
)

st.plotly_chart(
    fig_city,
    use_container_width=True
)
# ==========================================================
# TOP STATES
# ==========================================================

st.subheader("🗺 Top 10 States")

top_states = run_query("""
SELECT
    c.state,
    ROUND(SUM(oi.total_amount),2) AS revenue
FROM customers c
JOIN orders o
ON c.customer_id = o.customer_id
JOIN order_items oi
ON o.order_id = oi.order_id
GROUP BY c.state
ORDER BY revenue DESC
LIMIT 10;
""")

st.dataframe(
    top_states,
    use_container_width=True,
    hide_index=True
)

fig_state = px.bar(
    top_states,
    x="state",
    y="revenue",
    color="revenue",
    text="revenue",
    template="plotly_dark",
    title="Top States by Revenue"
)

st.plotly_chart(
    fig_state,
    use_container_width=True
)
# ==========================================================
# CUSTOMER LIFETIME VALUE
# ==========================================================

st.subheader("💎 Top 10 Customer Lifetime Value")

clv_df = run_query("""
SELECT
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    ROUND(SUM(oi.total_amount),2) AS lifetime_value
FROM customers c
JOIN orders o
ON c.customer_id = o.customer_id
JOIN order_items oi
ON o.order_id = oi.order_id
GROUP BY c.customer_id, customer_name
ORDER BY lifetime_value DESC
LIMIT 10;
""")

st.dataframe(
    clv_df,
    use_container_width=True,
    hide_index=True
)

fig_clv = px.bar(
    clv_df,
    x="customer_name",
    y="lifetime_value",
    color="lifetime_value",
    text="lifetime_value",
    template="plotly_dark",
    title="Top Customer Lifetime Value"
)

st.plotly_chart(
    fig_clv,
    use_container_width=True
)
# ==========================================================
# SALES BY DAY OF WEEK
# ==========================================================

st.subheader("📅 Sales by Day of Week")

day_sales = run_query("""
SELECT
    TO_CHAR(o.order_date, 'Day') AS day,
    ROUND(SUM(oi.total_amount),2) AS revenue
FROM orders o
JOIN order_items oi
ON o.order_id = oi.order_id
GROUP BY day
ORDER BY MIN(EXTRACT(DOW FROM o.order_date));
""")

fig_day = px.bar(
    day_sales,
    x="day",
    y="revenue",
    color="revenue",
    text="revenue",
    template="plotly_dark",
    title="Revenue by Day of Week"
)

st.plotly_chart(
    fig_day,
    use_container_width=True
)
# ==========================================================
# TOP BRANDS
# ==========================================================

st.subheader("🏷️ Top Brands")

top_brands = run_query("""
SELECT
    p.brand,
    ROUND(SUM(oi.total_amount),2) AS revenue
FROM order_items oi
JOIN products p
ON oi.product_id = p.product_id
GROUP BY p.brand
ORDER BY revenue DESC
LIMIT 10;
""")

st.dataframe(
    top_brands,
    use_container_width=True,
    hide_index=True
)

fig_brand = px.bar(
    top_brands,
    x="brand",
    y="revenue",
    color="revenue",
    text="revenue",
    template="plotly_dark",
    title="Top Brands by Revenue"
)

st.plotly_chart(
    fig_brand,
    use_container_width=True
)
# ============================================
# AI EXECUTIVE SUMMARY
# ============================================

st.subheader("🧠 AI Executive Summary")

with st.spinner("Generating executive summary..."):

    summary = generate_executive_summary(
        revenue,
        category_df,
        top_customers,
        orders_df
    )

st.success(summary)

pdf_file = generate_pdf_report(
    revenue,
    category_df,
    top_customers,
    summary
)

with open(pdf_file, "rb") as pdf:

    st.download_button(
        label="📄 Download AI Business Report",
        data=pdf,
        file_name="AI_Business_Report.pdf",
        mime="application/pdf"
    )
st.subheader("📧 Email Report")

email = st.text_input(
    "Recipient Email",
    placeholder="example@gmail.com"
)

if st.button("📨 Send Report"):

    if email.strip() == "":
        st.warning("Please enter an email address.")

    else:
        send_report(email, pdf_file)
        st.success("✅ Report sent successfully!")
# ============================================
# AI RECOMMENDATIONS
# ============================================

st.subheader("🎯 AI Business Recommendations")

recommendations = generate_recommendations(
    category_df,
    top_customers
)

for rec in recommendations:

    rec = rec.strip()

    if not rec:
        continue

    st.success(rec)
# ==========================================================
# AI BUSINESS HEALTH SCORE
# ==========================================================

st.subheader("🏅 AI Business Health Score")

score = 100

if len(category_df) > 0:
    if category_df.iloc[-1]["revenue"] < category_df["revenue"].mean():
        score -= 10

if len(top_customers) < 10:
    score -= 5

if revenue.iloc[0]["total"] < 100000:
    score -= 15

st.metric("Business Health", f"{score}/100")

if score >= 90:
    st.success("Excellent business performance.")
elif score >= 75:
    st.info("Business is performing well with room for improvement.")
else:
    st.warning("Business needs attention.")
# ==========================================================
# EXPORT DASHBOARD TO EXCEL
# ==========================================================

excel_buffer = BytesIO()

with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:

    category_df.to_excel(
        writer,
        sheet_name="Revenue by Category",
        index=False
    )

    top_customers.to_excel(
        writer,
        sheet_name="Top Customers",
        index=False
    )

orders_df = orders_df.copy()

if "month" in orders_df.columns:
    orders_df["month"] = pd.to_datetime(
        orders_df["month"]
    ).dt.tz_localize(None)

orders_df.to_excel(
    writer,
    sheet_name="Monthly Orders",
    index=False
)

excel_buffer.seek(0)

st.download_button(
    label="📊 Download Dashboard Excel",
    data=excel_buffer,
    file_name="AI_Dashboard_Report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
st.markdown("---")
st.subheader("📈 Sales Forecast")

import plotly.graph_objects as go

model, forecast_df, predicted_orders = forecast_sales(orders_df)

st.metric(
    "Predicted Next Month Orders",
    predicted_orders
)

forecast_plot = forecast_df.copy()

forecast_plot["Predicted"] = model.predict(forecast_plot[["x"]])

next_month = forecast_plot["month"].max() + pd.DateOffset(months=1)

forecast_plot = pd.concat([
    forecast_plot,
    pd.DataFrame({
        "month": [next_month],
        "orders": [None],
        "Predicted": [predicted_orders]
    })
])

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=forecast_plot["month"],
    y=forecast_plot["orders"],
    mode="lines+markers",
    name="Actual Orders"
))

fig.add_trace(go.Scatter(
    x=forecast_plot["month"],
    y=forecast_plot["Predicted"],
    mode="lines+markers",
    name="Forecast"
))

st.plotly_chart(fig, use_container_width=True)
st.markdown("---")

st.subheader("💰 Revenue Forecast")

revenue_df = run_query("""
SELECT
    DATE_TRUNC('month', o.order_date) AS month,
    SUM(oi.total_amount) AS revenue
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY 1
ORDER BY 1;
""")

from ai.revenue_forecast import forecast_revenue

model_rev, revenue_hist, predicted_revenue, growth = forecast_revenue(
    revenue_df
)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Predicted Next Month Revenue",
        f"₹{predicted_revenue:,.0f}"
    )

with col2:
    st.metric(
        "Expected Growth",
        f"{growth}%"
    )

revenue_plot = revenue_hist.copy()

revenue_plot["Predicted"] = model_rev.predict(
    revenue_plot[["x"]]
)

next_month = (
    revenue_plot["month"].max()
    + pd.DateOffset(months=1)
)

revenue_plot = pd.concat([
    revenue_plot,
    pd.DataFrame({
        "month": [next_month],
        "revenue": [None],
        "Predicted": [predicted_revenue]
    })
])

fig_rev = go.Figure()

fig_rev.add_trace(
    go.Scatter(
        x=revenue_plot["month"],
        y=revenue_plot["revenue"],
        mode="lines+markers",
        name="Actual Revenue"
    )
)

fig_rev.add_trace(
    go.Scatter(
        x=revenue_plot["month"],
        y=revenue_plot["Predicted"],
        mode="lines+markers",
        name="Forecast Revenue"
    )
)

st.plotly_chart(
    fig_rev,
    use_container_width=True
)
# ============================================
# AI CHATBOT
# ============================================

ai_chatbot()

st.markdown("---")

# ==========================================================
# FOOTER
# ==========================================================

st.caption(
    "🚀 AI E-Commerce Analytics Platform | "
    "Powered by Streamlit + PostgreSQL + Groq"
)