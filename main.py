import json
from bot.runner import run_strategy
from utils.broker import execute_order
from utils.logger import log_trade
from utils.telegram import send_telegram
from utils.paper import track_trade

def load_config():
    with open("config/config.json") as f:
        return json.load(f)

def main():
    config = load_config()
    mode = config.get("mode", "paper")

    for strat in config["strategies"]:
        if not strat.get("enabled", True):
            continue

        try:
            signal = run_strategy(strat)

            if signal == "buy":
                if mode == "paper":
                    track_trade(strat["symbol"], "buy", strat)
                else:
                    execute_order(strat["symbol"], "buy", strat)
                send_telegram(f"📈 BUY signal for {strat['symbol']} ({strat['name']})")

            elif signal == "sell":
                if mode == "paper":
                    track_trade(strat["symbol"], "sell", strat)
                else:
                    execute_order(strat["symbol"], "sell", strat)
                send_telegram(f"📉 SELL signal for {strat['symbol']} ({strat['name']})")

        except Exception as e:
            msg = f"⚠️ Error in {strat['name']}: {e}"
            print(msg)
            log_trade("error", strat["name"], str(e))
            send_telegram(msg)

if __name__ == "__main__":
    main()
    from scheduler.schedule_reports import run_scheduled_reports

    # ... your bot logic

    if __name__ == "__main__":
        try:
            # your bot start
            print("🚀 Bot running...")

            # run your bot loop/trading logic here

            run_scheduled_reports()

        except Exception as e:
            from utils.error_handler import notify_error
            notify_error(e, context="Live Bot Failure")
from scheduler import schedule_reports

if __name__ == "__main__":
    # Your trading bot logic...
    # run_strategy()

    # Start scheduler in background
    import threading
    threading.Thread(target=schedule_reports, daemon=True).start()

    # Optional: keep main alive
    while True:
        time.sleep(1)
