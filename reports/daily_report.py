from utils.emailer import send_email_report
from utils.discord import send_discord
import pandas as pd
import os
from datetime import datetime

def send_daily_report():
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = f"logs/trades_{today}.csv"

    if not os.path.exists(log_file):
        print(f"⚠️ No trades found for {today}")
        return

    trades_df = pd.read_csv(log_file)

    # Optional filter
    trades_df = trades_df[trades_df["confidence"].astype(float) >= 4]

    summary_lines = []
    for _, row in trades_df.iterrows():
        summary_lines.append(
            f"{row['symbol']} {row['action'].upper()} | Entry: {row['entry_price']} | Exit: {row.get('exit_price', 'N/A')} | Return: {row.get('return', 'N/A')} | Confidence: {row.get('confidence', 'N/A')}"
        )

    body = "\n".join(summary_lines)
    subject = f"📊 Daily Trade Summary – {today}"

    send_email_report(
        subject=subject,
        body=body,
        to_email=os.getenv("EMAIL_USER"),
        attachments=[log_file],
    )

    send_discord(f"📨 {subject}\n\n{body}")

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

