from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime


def generate_pdf_report(
    revenue,
    category_df,
    top_customers,
    ai_summary,
    filename="Business_Report.pdf"
):

    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(filename)

    story = []

    story.append(
        Paragraph(
            "<b>AI E-Commerce Business Report</b>",
            styles["Title"]
        )
    )

    story.append(
        Paragraph(
            datetime.now().strftime("%d %B %Y %H:%M"),
            styles["Normal"]
        )
    )

    story.append(Spacer(1,20))

    story.append(
        Paragraph(
            "<b>Total Revenue</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            f"₹ {float(revenue.iloc[0]['total']):,.2f}",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1,15))

    story.append(
        Paragraph(
            "<b>Top Revenue Categories</b>",
            styles["Heading2"]
        )
    )

    for _, row in category_df.head(5).iterrows():

        story.append(
            Paragraph(
                f"{row['category']} : ₹ {row['revenue']:,.2f}",
                styles["BodyText"]
            )
        )

    story.append(Spacer(1,15))

    story.append(
        Paragraph(
            "<b>Top Customers</b>",
            styles["Heading2"]
        )
    )

    for _, row in top_customers.head(5).iterrows():

        story.append(
            Paragraph(
                f"{row['customer_name']} : ₹ {row['spending']:,.2f}",
                styles["BodyText"]
            )
        )

    story.append(Spacer(1,15))

    story.append(
        Paragraph(
            "<b>AI Executive Summary</b>",
            styles["Heading2"]
        )
    )

    # Guard against a missing/failed AI summary so report generation
    # never crashes even if the AI call upstream returned None.
    safe_summary = ai_summary if ai_summary else "AI summary unavailable at this time."

    story.append(
        Paragraph(
            safe_summary.replace("\n", "<br/>"),
            styles["BodyText"]
        )
    )

    doc.build(story)

    return filename