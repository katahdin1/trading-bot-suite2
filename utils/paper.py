open_trades = []

def track_trade(symbol, side, config):
    trade = {
        "symbol": symbol,
        "side": side,
        "entry_price": 420,
        "target": config["profit_target"],
        "stop": config["stop_loss"]
    }
    open_trades.append(trade)
    print(f"📘 Paper trade opened: {trade}")

