import os
import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime

def send_email_report(subject, body, to_email, attachments=None):
    smtp_server = os.getenv("EMAIL_SERVER")
    smtp_port = int(os.getenv("EMAIL_PORT", 587))
    smtp_user = os.getenv("EMAIL_USER")
    smtp_pass = os.getenv("EMAIL_PASSWORD")

    msg = MIMEMultipart()
    msg["From"] = smtp_user
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    for file_path in attachments or []:
        try:
            with open(file_path, "rb") as f:
                part = MIMEApplication(f.read(), Name=os.path.basename(file_path))
                part["Content-Disposition"] = f"attachment; filename=\"{os.path.basename(file_path)}\""
                msg.attach(part)
        except Exception as e:
            print(f"⚠️ Error attaching {file_path}: {e}")

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
            print("✅ Email sent successfully.")
    except Exception as e:
        print(f"❌ Email failed: {e}")
