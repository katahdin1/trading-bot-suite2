from reports.generate_weekly_summary import generate_weekly_summary_pdf
from utils.emailer import send_email_report
from utils.telegram import send_telegram
from utils.discord import send_discord

def send_weekly_summary():
    output_path = "reports/weekly_summary.pdf"
    generate_weekly_summary_pdf(output_path)

    subject = "📊 Weekly Trading Summary"
    body = (
        "📈 **Weekly Performance Overview**\n"
        "- Total trades: 24\n"
        "- Win Rate: 62%\n"
        "- Net PnL: +$1,120\n"
        "- Best Strategy: SPY Momentum\n"
    )
    to_email = "your-email@example.com"  # TODO: Replace or use os.getenv
    attachments = [output_path]

    send_email_report(subject, body, to_email, attachments)
    send_telegram("📊 Weekly Summary Sent\n" + body)
    send_discord("📊 Weekly Summary Sent\n" + body)

