def spy_momentum_strategy(data):
  # Simple momentum strategy: Buy if close > MA, else Sell
  data["ma"] = data["Close"].rolling(window=20).mean()
  data["signal"] = data["Close"] > data["ma"]
  return data["signal"]
