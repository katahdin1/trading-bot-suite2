import os
from utils.emailer import send_email_report
from reports.generate_weekly_summary import generate_weekly_summary_pdf, generate_dummy_chart

def send_weekly_summary():
    generate_weekly_summary_pdf()
    generate_dummy_chart()

    subject = "📊 Weekly Strategy Summary Report"
    body = "Attached: PDF summary, equity chart & audit log."

    to_email = os.getenv("EMAIL_USER")

    attachments = [
        "reports/weekly_summary.pdf",
        "charts/equity_curve.png",
        "logs/trades.csv"
    ]

    send_email_report(subject, body, to_email, attachments)
from utils.telegram import send_telegram

# after send_email_report(...)
send_telegram("📬 Weekly summary emailed with chart + audit.")

