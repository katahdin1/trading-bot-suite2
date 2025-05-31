from reports.daily_report import send_daily_trade_report
from reports.weekly_report import send_weekly_summary

print("📤 Sending test daily report...")
send_daily_trade_report()
print("✅ Email sent successfully.")

print("📤 Sending test weekly summary...")
send_weekly_summary()
print("✅ Email sent successfully.")
