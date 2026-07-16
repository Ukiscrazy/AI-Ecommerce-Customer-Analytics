import streamlit as st
import pandas as pd
import plotly.express as px

from ai.sql_agent import generate_sql
from ai.query_executor import execute_sql
from ai.chatbot import ask_groq


INSIGHT_SYSTEM_PROMPT = (
    "You are a senior business analyst. "
    "Write clear, concise business insights in plain English. "
    "Never return SQL or code — only prose."
)


# ==========================================================
# AI CHATBOT
# ==========================================================

def ai_chatbot():

    st.markdown("---")
    st.header("🤖 AI Business Assistant")
    st.caption("Ask questions in plain English and get business insights.")

    # ------------------------------------------------------

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "question_input" not in st.session_state:
        st.session_state.question_input = ""

    # ------------------------------------------------------
    # SUGGESTED QUESTIONS
    # ------------------------------------------------------

    st.markdown("### 💡 AI Suggested Questions")

    suggested_questions = [
        "🏆 Top 10 Customers",
        "📈 Monthly Sales",
        "💰 Revenue by Category",
        "🛒 Best Selling Products",
        "🏙 Highest Revenue City",
        "📦 Total Orders",
        "📊 Average Order Value",
        "⭐ Top 5 Products by Revenue",
        "🎯 Highest Spending Customer",
        "📉 Lowest Selling Products"
    ]

    mapping = {
        "🏆 Top 10 Customers": "Show top 10 customers by spending",
        "📈 Monthly Sales": "Show monthly sales",
        "💰 Revenue by Category": "Which category generated the highest revenue?",
        "🛒 Best Selling Products": "Show top 10 best selling products",
        "🏙 Highest Revenue City": "Which city generated the highest revenue?",
        "📦 Total Orders": "How many total orders are there?",
        "📊 Average Order Value": "What is the average order value?",
        "⭐ Top 5 Products by Revenue": "Show top 5 products by revenue",
        "🎯 Highest Spending Customer": "Who is the highest spending customer?",
        "📉 Lowest Selling Products": "Show lowest selling products"
    }

    cols = st.columns(2)

    for i, question_text in enumerate(suggested_questions):

        with cols[i % 2]:

            if st.button(question_text, use_container_width=True, key=f"suggest_{i}"):
                st.session_state.question_input = mapping[question_text]

    # ------------------------------------------------------
    # QUESTION INPUT
    # ------------------------------------------------------

    question = st.text_input(
        "Ask your business question",
        value=st.session_state.question_input,
        placeholder="Example: Which category generated the highest revenue?"
    )

    if st.button("🚀 Ask AI", use_container_width=True):

        if question.strip() == "":
            st.warning("Please enter a question.")
        else:
            with st.spinner("Generating SQL..."):
                sql = generate_sql(question)

            if sql is None:
                st.error("Failed to generate SQL.")
            else:
                result = execute_sql(sql)

                st.session_state.chat_history.insert(
                    0,
                    {
                        "question": question,
                        "sql": sql,
                        "result": result
                    }
                )

    # ------------------------------------------------------
    # RECENT QUERIES
    # ------------------------------------------------------

    st.subheader("🕒 Recent Queries")

    if len(st.session_state.chat_history) > 0:

        recent = [x["question"] for x in st.session_state.chat_history[:5]]

        selected = st.selectbox(
            "Quick Open",
            ["Select a previous query"] + recent
        )

        if st.button("🔄 Load Query"):
            if selected != "Select a previous query":
                st.session_state.question_input = selected
                st.rerun()

    else:
        st.info("No recent queries yet.")

    # ------------------------------------------------------
    # RENDER CHAT HISTORY
    # ------------------------------------------------------

    st.markdown("---")

    for idx, chat in enumerate(st.session_state.chat_history):

        st.markdown(f"### 👤 {chat['question']}")

        st.code(chat["sql"], language="sql")

        df = chat["result"]

        if df is None:
            st.error("Database Error")
            continue

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇ Download CSV",
            data=csv,
            file_name="result.csv",
            mime="text/csv",
            key=f"csv_{idx}"
        )

        st.markdown("### 📊 Visualization")

        if (
            len(df.columns) == 2
            and pd.api.types.is_numeric_dtype(df.iloc[:, 1])
        ):

            x = df.columns[0]
            y = df.columns[1]

            try:

                if "month" in x.lower() or "date" in x.lower():
                    fig = px.line(
                        df,
                        x=x,
                        y=y,
                        markers=True,
                        template="plotly_dark"
                    )

                elif len(df) <= 8:
                    fig = px.pie(
                        df,
                        names=x,
                        values=y,
                        template="plotly_dark"
                    )

                else:
                    fig = px.bar(
                        df,
                        x=x,
                        y=y,
                        color=y,
                        template="plotly_dark"
                    )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    key=f"chart_{idx}"
                )

            except Exception:
                pass

        st.markdown("### 💡 AI Business Insight")

        with st.spinner("Analyzing..."):

            prompt = f"""
You are a senior business analyst.

Question:
{chat['question']}

SQL Result:
{df.head(20).to_string(index=False)}

Give 3 short business insights.
"""

            try:
                insight = ask_groq(prompt, system_prompt=INSIGHT_SYSTEM_PROMPT)
                if insight is None:
                    insight = "Unable to generate insights."
            except Exception:
                insight = "Unable to generate insights."

        st.success(insight)

        st.markdown("---")

    # ------------------------------------------------------
    # CLEAR CHAT
    # ------------------------------------------------------

    if st.session_state.chat_history:

        left, right = st.columns([1, 5])

        with left:
            if st.button("🗑 Clear Chat"):
                st.session_state.chat_history = []
                st.session_state.question_input = ""
                st.rerun()

    st.caption(
        "🚀 AI E-Commerce Analytics | Powered by Groq + PostgreSQL + Streamlit"
    )

    st.markdown("---")