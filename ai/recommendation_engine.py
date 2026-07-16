from ai.chatbot import ask_groq


def generate_recommendations(category_df, top_customers):

    prompt = f"""
You are a senior business consultant.

Revenue by Category:

{category_df.to_string(index=False)}

Top Customers:

{top_customers.head(10).to_string(index=False)}

Give exactly 5 short business recommendations.

Each recommendation should be one line.

Focus on:
- Revenue growth
- Inventory
- Marketing
- Customer retention
- Profit
"""

    recommendations = ask_groq(prompt)

    return recommendations.split("\n")