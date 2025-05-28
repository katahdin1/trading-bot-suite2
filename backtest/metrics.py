def calculate_pnl(trades):
    wins = [t for t in trades if t['result'] == 'win']
    losses = [t for t in trades if t['result'] == 'loss']
    win_rate = len(wins) / len(trades) if trades else 0
    profit = sum(t['pnl'] for t in trades)
    avg_return = profit / len(trades) if trades else 0

    return {
        'trades': len(trades),
        'wins': len(wins),
        'losses': len(losses),
        'win_rate': round(win_rate * 100, 2),
        'net_profit': round(profit, 2),
        'avg_return_per_trade': round(avg_return, 2)
    }

