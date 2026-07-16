import pandas as pd
from ai.chatbot import ask_groq


def generate_executive_summary(
    revenue_df,
    category_df,
    customer_df,
    orders_df
):
    """
    Uses Groq AI to generate an executive business summary.
    """

    prompt = f"""
You are a Senior Business Intelligence Analyst.

Analyze the following business data.

TOTAL REVENUE

{revenue_df.to_string(index=False)}

--------------------------------------------

REVENUE BY CATEGORY

{category_df.head(10).to_string(index=False)}

--------------------------------------------

TOP CUSTOMERS

{customer_df.head(10).to_string(index=False)}

--------------------------------------------

MONTHLY ORDERS

{orders_df.head(12).to_string(index=False)}

--------------------------------------------

Generate:

1. Executive Summary
2. Key Findings
3. Business Risks
4. Growth Opportunities
5. Final Recommendation

Rules:
- Keep it professional.
- Use bullet points.
- Keep it concise.
- Maximum 200 words.
"""

    try:

        summary = ask_groq(prompt)

        return summary

    except Exception as e:

        return f"Error generating AI summary:\n\n{e}"