# utils/mock_broker.py

from datetime import datetime
import random

def simulate_option_order(symbol, side, option_type, strike, expiry, quantity=1, target=0.10, stop=0.05, trailing_stop=None, breakeven_trigger=None):
    entry_price = round(random.uniform(1.0, 3.0), 2)  # Mock premium
    max_price = entry_price
    current_price = entry_price
    breakeven_locked = False

    for i in range(20):  # Simulate 20 time steps
        move = random.uniform(-0.05, 0.05)
        current_price = round(max(0.01, current_price + move), 2)
        max_price = max(max_price, current_price)

        if breakeven_trigger and not breakeven_locked and (max_price - entry_price) >= breakeven_trigger:
            stop = 0.0  # move stop to breakeven
            breakeven_locked = True

        if trailing_stop:
            trailing_price = max_price - trailing_stop
            if current_price <= trailing_price:
                break

        if (side == "buy" and current_price >= entry_price + target) or \
           (side == "sell" and current_price <= entry_price - target):
            break

        if (side == "buy" and current_price <= entry_price - stop) or \
           (side == "sell" and current_price >= entry_price + stop):
            break

    exit_price = current_price

    return {
        "symbol": symbol,
        "side": side,
        "type": option_type,
        "strike": strike,
        "expiry": expiry,
        "entry_price": entry_price,
        "exit_price": exit_price,
        "quantity": quantity,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
