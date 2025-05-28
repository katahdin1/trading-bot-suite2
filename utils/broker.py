def execute_order(symbol, side, config):
    print(f"🚀 LIVE ORDER: {side.upper()} {symbol} | PT={config['profit_target']} SL={config['stop_loss']}")

