# metrics/calculate_pnl.py

def calculate_pnl(trades):
    """
    Calculate performance metrics from a list of trades.

    Each trade is expected to be a dictionary with at least:
        - 'pnl' (float): profit or loss

    Returns:
        dict: Summary of performance metrics.
    """
    total_trades = len(trades)
    wins = [t for t in trades if t["pnl"] > 0]
    losses = [t for t in trades if t["pnl"] <= 0]

    net_profit = sum(t["pnl"] for t in trades)
    avg_return = net_profit / total_trades if total_trades else 0
    win_rate = len(wins) / total_trades if total_trades else 0

    return {
        "trades": total_trades,
        "wins": len(wins),
        "losses": len(losses),
        "win_rate": round(win_rate * 100, 2),
        "net_profit": round(net_profit, 2),
        "avg_return_per_trade": round(avg_return, 2),
    }
