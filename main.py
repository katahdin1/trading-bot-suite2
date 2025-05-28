import json
import time
import threading
from datetime import datetime

from bot.runner import run_strategy
from scheduler.schedule_runner import start_scheduler
from utils.telegram import send_telegram
from utils.discord import send_discord
from utils.mock_broker import simulate_option_order
from utils.logger import log_trade


def load_config():
    with open("config/config.json") as f:
        return json.load(f)


def format_trade_message(trade):
    return (
        f"📈 MOCK OPTION TRADE\n"
        f"Symbol: {trade['symbol']}\n"
        f"Type: {trade['type'].upper()} | Strike: {trade['strike']} | Expiry: {trade['expiry']}\n"
        f"Side: {trade['side'].upper()} | Qty: {trade['quantity']}\n"
        f"Entry: ${trade['entry_price']:.2f} → Exit: ${trade['exit_price']:.2f}\n"
        f"Time: {trade['timestamp']}"
    )


def run_bot():
    config = load_config()
    mode = config.get("mode", "paper")

    for strat in config["strategies"]:
        if not strat.get("enabled", True):
            continue

        try:
            signal = run_strategy(strat)

            if signal in ["buy", "sell"]:
                # ✅ PAPER MODE = SIMULATED OPTIONS TRADE
                if mode == "paper":
                    trade = simulate_option_order(
                        symbol=strat["symbol"],
                        side=signal,
                        option_type=strat.get("type", "call"),
                        strike=strat.get("strike", 430),
                        expiry=strat.get("expiry", "2025-06-21"),
                        quantity=strat.get("quantity", 1),
                        target=strat.get("target", 0.20),
                        stop=strat.get("stop", 0.10),
                        trailing_stop=strat.get("trailing_stop", 0.08),
                        breakeven_trigger=strat.get("breakeven_trigger", 0.12)
                    )

                    msg = format_trade_message(trade)
                    send_telegram(msg)
                    send_discord(msg)
                    log_trade("mock_option", strat["name"], msg)

                else:
                    # ❗️LIVE BROKER: plug in real `execute_order()` here when ready
                    pass

        except Exception as e:
            msg = f"⚠️ Error in {strat['name']}: {e}"
            print(msg)
            log_trade("error", strat["name"], str(e))
            send_telegram(msg)
            send_discord(msg)


if __name__ == "__main__":
    print("🚀 Bot starting...")
    threading.Thread(target=start_scheduler, daemon=True).start()

    while True:
        run_bot()
        time.sleep(60)  # Adjust this interval as needed
