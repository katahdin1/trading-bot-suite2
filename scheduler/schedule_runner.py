import schedule
import time
from backtest.simulate import run_simulation
from reports.daily_report import send_daily_trade_report
from reports.weekly_report import send_weekly_summary
from utils.telegram import send_telegram

def job_simulation():
    run_simulation()
    send_telegram("📈 Simulation executed via scheduler.")

def job_daily():
    send_daily_trade_report()
    send_telegram("🗓 Daily report sent.")

def job_weekly():
    send_weekly_summary()
    send_telegram("📊 Weekly summary sent.")

def start_scheduler():
    # Schedule jobs at specific times
    schedule.every().day.at("16:00").do(job_simulation)
    schedule.every().day.at("16:10").do(job_daily)
    schedule.every().friday.at("16:30").do(job_weekly)

    print("✅ Scheduler running...")

    while True:
        schedule.run_pending()
        time.sleep(1)

# Allow this file to run standalone too
if __name__ == "__main__":
    start_scheduler()
