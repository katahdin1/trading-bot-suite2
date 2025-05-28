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
