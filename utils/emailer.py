import smtplib
import ssl
import os
from email.message import EmailMessage

def send_email_report(subject, body, to_email, attachments=[], smtp_server="smtp.gmail.com", port=465):
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")

    if not sender_email or not sender_password:
        print("❌ EMAIL_USER or EMAIL_PASS is not set. Please check your .env file.")
        return

    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    for file_path in attachments:
        try:
            with open(file_path, "rb") as f:
                file_data = f.read()
                filename = file_path.split("/")[-1]
                msg.add_attachment(
                    file_data,
                    maintype="application",
                    subtype="octet-stream",
                    filename=filename
                )
        except Exception as e:
            print(f"⚠️ Error attaching {file_path}: {e}")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, sender_password)
        server.send_message(msg)
        print("✅ Email sent successfully.")
