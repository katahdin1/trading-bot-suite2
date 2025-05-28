def evaluate_strategy(data):
  # Sample PnL evaluation logic
  trades = len(data)
  wins = (data["return"] > 0).sum()
  losses = trades - wins
  win_rate = wins / trades if trades > 0 else 0
  net_profit = data["return"].sum()
  avg_return = data["return"].mean() if trades > 0 else 0

  return {
      "trades": trades,
      "wins": wins,
      "losses": losses,
      "win_rate": round(win_rate, 4),
      "net_profit": round(net_profit, 2),
      "avg_return_per_trade": round(avg_return, 2),
  }
