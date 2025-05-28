from backtest.data import get_spy_data
from strategy.spy_momentum import spy_momentum_strategy

def run_backtest():
    df = get_spy_data()
    trades = []
    position = None

    for i in range(20, len(df)):
        window = df.iloc[:i]
        signal = spy_momentum_strategy(window)

        if signal == "buy" and not position:
            position = df.iloc[i]["Close"]
            trades.append({"type": "buy", "price": position})

        elif signal == "sell" and position:
            exit_price = df.iloc[i]["Close"]
            trades.append({
                "type": "sell", "price": exit_price,
                "pnl": round(exit_price - position, 2)
            })
            position = None

    wins = [t["pnl"] for t in trades if t.get("pnl", 0) > 0]
    losses = [t["pnl"] for t in trades if t.get("pnl", 0) <= 0]

    print(f"📈 Total Trades: {len(trades)}")
    print(f"✅ Wins: {len(wins)} | ❌ Losses: {len(losses)}")
    print(f"💰 Net PnL: {sum(t.get('pnl', 0) for t in trades)}")

if __name__ == "__main__":
    run_backtest()
