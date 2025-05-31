import csv
import os
from datetime import datetime

def log_trade(action, strategy, price, extra=None):
    date = datetime.now().strftime("%Y-%m-%d")
    os.makedirs("logs", exist_ok=True)
    path = f"logs/trades_{date}.csv"
    row = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "strategy": strategy,
        "price": price,
        **(extra or {})
    }

    write_header = not os.path.exists(path)
    with open(path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if write_header:
            writer.writeheader()
        writer.writerow(row)
