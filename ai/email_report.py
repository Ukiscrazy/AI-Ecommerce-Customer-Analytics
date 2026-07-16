import yagmail


def send_report(receiver_email, pdf_path):
    sender_email = "umeshkushwaha431511@gmail.com"
    app_password = "baijnath123@"

    yag = yagmail.SMTP(sender_email, app_password)

    yag.send(
        to=receiver_email,
        subject="AI E-Commerce Business Report",
        contents="Please find the attached AI Business Report.",
        attachments=pdf_path
    )

    return True