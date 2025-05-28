# utils/logger.py
import csv
import os
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def log_trade(action, strategy, details):
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{LOG_DIR}/{date_str}.csv"

    file_exists = os.path.isfile(filename)
    with open(filename, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "action", "strategy", "details"])

        writer.writerow([
            datetime.now().isoformat(),
            action,
            strategy,
            details
        ])
