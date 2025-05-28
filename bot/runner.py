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

