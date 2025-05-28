# utils/pdt_guard.py
import os
import csv
from datetime import datetime, timedelta

LOG_DIR = "logs"

def count_day_trades():
    today = datetime.now().date()
    past_5_days = [today - timedelta(days=i) for i in range(5)]
    count = 0

    for date in past_5_days:
        path = f"{LOG_DIR}/{date.isoformat()}.csv"
        if os.path.exists(path):
            with open(path, newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["action"] in ["buy", "sell"]:
                        count += 1
    return count

def is_pdt_safe():
    return count_day_trades() < 3
