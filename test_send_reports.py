from reports.daily_report import send_daily_trade_report
from reports.weekly_report import send_weekly_summary

if __name__ == "__main__":
    print("📤 Sending test daily report...")
    send_daily_trade_report()

    print("📤 Sending test weekly summary...")
    send_weekly_summary()
