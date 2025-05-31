def spy_rsi_strategy(symbol, strat):
  import yfinance as yf
  import pandas as pd
  import ta

  df = yf.download(symbol, period="15d", interval="30m", progress=False)
  df["RSI"] = ta.momentum.RSIIndicator(df["Close"], window=14).rsi()

  confidence = 0
  latest = df.iloc[-1]
  prev = df.iloc[-2]

  if latest["RSI"] > 50: confidence += 1
  if prev["RSI"] < 30 and latest["RSI"] > 30: confidence += 2
  if latest["Close"] > df["Close"].rolling(20).mean().iloc[-1]: confidence += 1

  signal = "buy" if confidence >= 3 else None

  meta = {
      "entry_price": float(latest["Close"]),
      "target": float(latest["Close"]) * strat.get("profit_target", 1.05),
      "stop": float(latest["Close"]) * strat.get("stop", 0.97)
  }

  return signal, confidence, meta
