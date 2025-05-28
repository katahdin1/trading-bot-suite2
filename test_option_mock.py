# test_option_mock.py

from utils.mock_broker import simulate_option_order

order = simulate_option_order(
    symbol="SPY",
    side="buy",
    option_type="call",
    strike=430,
    expiry="2025-06-21",
    quantity=1,
    target=0.15,
    stop=0.05,
    trailing_stop=0.10,
    breakeven_trigger=0.10
)

print("✅ Final simulated order result:")
print(order)
# test_option_mock.py

from utils.mock_broker import simulate_option_order
from utils.discord import send_discord

order = simulate_option_order(
    symbol="SPY",
    side="buy",
    option_type="call",
    strike=430,
    expiry="2025-06-21",
    quantity=1,
    target=0.15,
    stop=0.05,
    trailing_stop=0.10,
    breakeven_trigger=0.10
)

summary = (
    f"🧪 Simulated Option Trade\n"
    f"Symbol: {order['symbol']}\n"
    f"Type: {order['type']} {order['strike']} {order['expiry']}\n"
    f"Side: {order['side'].upper()}\n"
    f"Entry: ${order['entry_price']:.2f}\n"
    f"Exit: ${order['exit_price']:.2f}\n"
    f"Quantity: {order['quantity']}\n"
    f"Time: {order['timestamp']}"
)

send_discord(summary)
print("✅ Discord alert sent.")
