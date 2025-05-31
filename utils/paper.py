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
exit_msg = (
    f"📤 EXIT TRADE\n"
    f"Symbol: {symbol}\n"
    f"Type: {strat.get('type', 'stock')}\n"
    f"Strike: {strat.get('strike')}\n"
    f"Expiry: {strat.get('expiry')}\n"
    f"Exit Price: {exit_price}\n"
    f"Reason: {'Take Profit' if exit_price >= strat['take_profit'] else 'Stop Loss'}"
)

send_telegram(exit_msg)
send_discord(exit_msg)

