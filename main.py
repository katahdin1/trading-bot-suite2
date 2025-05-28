import json
import time
import threading

from bot.runner import run_strategy
from utils.broker import execute_order
from utils.logger import log_trade
from utils.telegram import send_telegram
from utils.discord import send_discord
from utils.paper import track_trade
from scheduler.schedule_runner import start_scheduler

# ✅ Format buy/sell messages
def format_trade_message(signal, strat):
    msg = (
        f"{'📈' if signal == 'buy' else '📉'} {signal.upper()} SIGNAL\n"
        f"Symbol: {strat['symbol']}\n"
        f"Strategy: {strat['name']}\n"
        f"Quantity: {strat.get('quantity', 1)}\n"
        f"Entry: {strat.get('entry_price', 'MKT')}\n"
        f"Target: {strat.get('target', 'N/A')}\n"
        f"Stop: {strat.get('stop', 'N/A')}"
    )

    if strat.get("type") in ["call", "put"]:
        msg += (
            f"\nStrike: {strat.get('strike')} {strat['type'].upper()}"
            f"\nExpiry: {strat.get('expiry')}"
        )

    return msg


def load_config():
    with open("config/config.json") as f:
        return json.load(f)


def run_bot():
    config = load_config()
    mode = config.get("mode", "paper")

    for strat in config["strategies"]:
        if not strat.get("enabled", True):
            continue

        try:
            signal = run_strategy(strat)

            if signal in ["buy", "sell"]:
                if mode == "paper":
                    track_trade(strat["symbol"], signal, strat)
                else:
                    execute_order(strat["symbol"], signal, strat)

                # ✅ Generate message
                msg = format_trade_message(signal, strat)

                # ✅ Send alerts
                send_telegram(msg)
                send_discord(msg)

                # ✅ Log trade
                log_trade(signal, strat["name"], msg)

        except Exception as e:
            msg = f"⚠️ Error in {strat['name']}: {e}"
            print(msg)
            log_trade("error", strat["name"], str(e))
            send_telegram(msg)
            send_discord(msg)


if __name__ == "__main__":
    print("🚀 Bot starting...")

    # ✅ Start report scheduler
    threading.Thread(target=start_scheduler, daemon=True).start()

    # ✅ Continuous bot loop
    while True:
        run_bot()
        time.sleep(60)
