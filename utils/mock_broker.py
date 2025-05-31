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
import random
from utils.discord import send_discord

def simulate_option_order(order):
    entry_price = order.get("entry_price", 2.0)
    direction = order.get("type", "call")

    current_price = entry_price
    max_price = current_price
    stop_pct = 0.10
    target_pct = 0.20

    for _ in range(5):  # Simulate price ticks
        change = random.uniform(-0.05, 0.1)
        current_price += change
        max_price = max(max_price, current_price)

        trailing_stop = max_price * (1 - stop_pct)
        if current_price <= trailing_stop or current_price >= entry_price * (1 + target_pct):
            break

    order.update({
        "exit_price": round(current_price, 2),
        "return": round(current_price - entry_price, 2)
    })
    send_discord(f"🎯 Simulated Option Exit: {order}")
    return order
simulate_option_order({
    "symbol": "SPY", "type": "call", "strike": 430,
    "expiry": "2025-06-21", "entry_price": 2.0
})
