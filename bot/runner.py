import random

def run_strategy(config):
    price = random.uniform(410, 430)
    ma = 420  # Placeholder moving average
    print(f"{config['name']}: Price={price:.2f}, MA={ma:.2f}")

    if price > ma + 1:
        return "buy"
    elif price < ma - 1:
        return "sell"
    return "hold"
from reports.daily_report import send_daily_trade_report
from reports.weekly_report import send_weekly_summary

# Daily end-of-day trigger
send_daily_trade_report()

# Weekly trigger (e.g., every Friday)
import datetime
if datetime.datetime.today().weekday() == 4:  # Friday
    send_weekly_summary()

