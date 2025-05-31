import json
import time
import threading

from bot.runner import run_strategy
from utils.logger import log_trade
from utils.telegram import send_telegram
from utils.discord import send_discord
from utils.paper import track_trade
from scheduler.schedule_runner import start_scheduler


def load_config():
    with open("config/config.json") as f:
        return json.load(f)


def format_trade_message(signal, strat, confidence=None):
    msg = f"{'📈' if signal == 'buy' else '📉'} {signal.upper()} SIGNAL"

    if confidence is not None:
        msg += f" (Confidence: {confidence}/5)"

    msg += (
        f"\nSymbol: {strat['symbol']}"
        f"\nStrategy: {strat['name']}"
        f"\nQuantity: {strat.get('quantity', 1)}"
        f"\nEntry: {strat.get('entry_price', 'MKT')}"
        f"\nTarget: {strat.get('target', 'N/A')}"
        f"\nStop: {strat.get('stop', 'N/A')}"
    )

    if strat.get("type") in ["call", "put"]:
        msg += (
            f"\nStrike: {strat.get('strike')} {strat['type'].upper()}"
            f"\nExpiry: {strat.get('expiry')}"
        )

    return msg


def run_bot(live_mode="paper", strategy_key=None, strict=False):
    from config.config_loader import load_strategy_config
    from executor.trade_executor import execute_trade
    from strategies.registry import strategy_lookup
    from utils.discord import send_discord
    from utils.telegram import send_telegram
    from utils.logger import log_trade
    from data.price import get_latest_price

    config = load_strategy_config()

    for strat in config["strategies"]:
        if not strat.get("enabled"):
            continue

        if strategy_key and strat["name"] != strategy_key:
            continue

        strategy_func = strategy_lookup.get(strat["name"])
        if not strategy_func:
            continue

        try:
            symbol = strat.get("symbol", "SPY")
            price = get_latest_price(symbol)
            signal, confidence, meta = strategy_func(symbol, strat)

            # 🚫 Strict mode: skip low-confidence trades
            if strict and confidence < 4:
                msg = f"⚠️ Skipping {strat['name']} – Confidence {confidence} < 4"
                send_discord(msg)
                send_telegram(msg)
                log_trade("skipped", strat["name"], "Low confidence", extra={"confidence": confidence})
                continue

            if signal in ["buy", "sell"]:
                msg = format_trade_message(signal, strat, confidence)
                send_discord(msg)
                send_telegram(msg)
                log_trade(signal, strat["name"], price, extra={"confidence": confidence})
                execute_trade(signal, symbol, live_mode, strat, meta)

        except Exception as e:
            err_msg = f"⚠️ Error in {strat['name']}: {e}"
            send_discord(err_msg)
            send_telegram(err_msg)


if __name__ == "__main__":
    print("🚀 Bot starting...")

    # Start daily/weekly scheduler
    threading.Thread(target=start_scheduler, daemon=True).start()

    # Run main bot loop
    while True:
        run_bot()
        time.sleep(60)  # ⏲ Adjust for desired frequency
