import os
import csv
from datetime import datetime

def log_trade(signal, strategy_name, details):
    date_str = datetime.now().strftime("%Y-%m-%d")
    log_dir = "logs"
    log_file = os.path.join(log_dir, f"{date_str}.csv")

    os.makedirs(log_dir, exist_ok=True)

    file_exists = os.path.isfile(log_file)
    with open(log_file, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "signal", "strategy", "details"])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            signal,
            strategy_name,
            details
        ])
