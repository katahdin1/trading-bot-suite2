from utils.emailer import send_email_report
from utils.telegram import send_telegram
from utils.discord import send_discord

def send_daily_trade_report():
    subject = "📩 Daily Trade Report"
    body = (
        "🗓 **Daily Summary**\n"
        "- Total trades: 5\n"
        "- Wins: 3\n"
        "- Losses: 2\n"
        "- Net PnL: +$420\n"
        "- Strategy: SPY Momentum\n"
    )
    to_email = "your-email@example.com"  # TODO: Replace or use os.getenv
    from datetime import datetime
    log_file = f"logs/{datetime.now().strftime('%Y-%m-%d')}.csv"
    attachments = [log_file] if os.path.exists(log_file) else []
  # Optional, replace with actual path

    # Send via all channels
    send_email_report(subject, body, to_email, attachments)
    send_telegram(f"✅ Daily Report Sent\n{body}")
    send_discord(f"✅ Daily Report Sent\n{body}")
import os
from datetime import datetime
from utils.emailer import send_email_report
from utils.discord import send_discord

def send_daily_trade_report():
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = f"logs/{today}.csv"

    subject = f"📈 Daily Trade Report – {today}"
    body = f"Attached is your trading activity for {today}.\n\n✅ Summary:\n- Log file: {log_file}"
    to_email = os.getenv("EMAIL_USER")

    attachments = []
    if os.path.exists(log_file):
        attachments.append(log_file)
    else:
        body += "\n⚠️ No trades were logged today."

    send_email_report(subject, body, to_email, attachments)
    send_discord(f"📬 Daily trade report sent for `{today}`.")

