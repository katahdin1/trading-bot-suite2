# test_email.py
from utils.emailer import send_email_report

send_email_report(
    subject="📧 Test Email",
    body="This is a test email from your trading bot setup.",
    to_email="kysenick@gmail.com"  # ← Replace with your real email
)
