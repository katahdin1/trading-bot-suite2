import traceback
from utils.emailer import send_email_report
import os

def notify_error(err, context=""):
    subject = "⚠️ Bot Error Alert"
    body = f"Context: {context}\n\nTraceback:\n{traceback.format_exc()}"
    to_email = os.getenv("EMAIL_USER")
    send_email_report(subject, body, to_email)
try:
    # some code
except Exception as e:
    from utils.error_handler import notify_error
    notify_error(e, context="Trade Execution Block")
