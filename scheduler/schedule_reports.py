import schedule
import time
from reports.daily_report import send_daily_trade_report
from reports.weekly_report import send_weekly_summary
from utils.telegram import send_telegram

def schedule_reports():
    def daily():
        send_daily_trade_report()
        send_telegram("📬 Daily report sent.")

    def weekly():
        send_weekly_summary()
        send_telegram("📬 Weekly summary sent.")

    schedule.every().day.at("18:00").do(daily)
    schedule.every().friday.at("18:00").do(weekly)

    print("📅 Report scheduler started...")

    while True:
        schedule.run_pending()
        time.sleep(60)
from utils.telegram import send_telegram

send_telegram("✅ GitHub Action: Reports generated and emailed.")

