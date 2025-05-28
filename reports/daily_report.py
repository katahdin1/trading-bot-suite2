import os
from utils.emailer import send_email_report

def send_daily_trade_report(log_path="logs/trades.csv"):
    subject = "📈 Daily Trade Report"
    body = "Attached is today's trade log and chart."

    to_email = os.getenv("EMAIL_USER")
    attachments = [log_path]

    if os.path.exists("charts/sharpe_curve.png"):
        attachments.append("charts/sharpe_curve.png")

    send_email_report(subject, body, to_email, attachments)
from utils.telegram import send_telegram

# after send_email_report(...)
send_telegram("📬 Daily trade report emailed successfully.")