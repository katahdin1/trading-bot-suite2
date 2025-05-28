import schedule
import time
from backtest.simulate import run_simulation
from reports.daily_report import send_daily_trade_report
from reports.weekly_report import send_weekly_summary
from utils.telegram import send_telegram
from utils.discord import send_discord

def job_simulation():
    run_simulation()
    send_telegram("📈 Simulation run via scheduler.")
    send_discord("📈 Simulation run via scheduler.")

def job_daily():
    send_daily_trade_report()

def job_weekly():
    send_weekly_summary()

def start_scheduler():
    schedule.every().day.at("16:00").do(job_simulation)
    schedule.every().day.at("16:10").do(job_daily)
    schedule.every().friday.at("16:30").do(job_weekly)

    print("✅ Scheduler running...")

    while True:
        schedule.run_pending()
        time.sleep(1)

