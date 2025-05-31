import pandas as pd

def spy_options_strategy(data):
    data = data.copy()
    data["MA_20"] = data["Close"].rolling(window=20).mean()
    data["RSI"] = compute_rsi(data["Close"], window=14)
    data["Avg_Volume"] = data["Volume"].rolling(window=20).mean()

    trades = []

    for i in range(1, len(data)):
        row = data.iloc[i]
        prev = data.iloc[i - 1]

        close = float(row["Close"])
        prev_close = float(prev["Close"])
        ma = float(row["MA_20"])
        prev_ma = float(prev["MA_20"])
        volume = float(row["Volume"])
        avg_volume = float(row["Avg_Volume"])
        rsi = float(row["RSI"])

        # === Confidence Score ===
        confidence = 0
        confidence += int(close > ma)
        confidence += int(volume > avg_volume)
        confidence += int(rsi > 50)

        # Add mock IV (if real data is available, replace this line)
        iv = 0.30  # TODO: replace with real options IV
        confidence += int(iv > 0.25)

        # === Filter out weak setups ===
          if confidence < 4:

            continue

        # === Entry condition: breakout logic ===
        if prev_close < prev_ma and close > ma:
            entry_price = 2.00
            exit_price = 2.30  # 15% gain

            if (exit_price - entry_price) / entry_price >= 0.10:
                trades.append({
                    "date": row.name,
                    "symbol": "SPY",
                    "type": "call",
                    "strike": round(close * 1.01),
                    "expiry": (row.name + pd.Timedelta(days=7)).strftime("%Y-%m-%d"),
                    "entry_price": entry_price,
                    "exit_price": exit_price,
                    "return": exit_price - entry_price,
                    "side": "buy",
                    "confidence": confidence
                })

        elif prev_close > prev_ma and close < ma:
            entry_price = 2.00
            exit_price = 2.30

            if (exit_price - entry_price) / entry_price >= 0.10:
                trades.append({
                    "date": row.name,
                    "symbol": "SPY",
                    "type": "put",
                    "strike": round(close * 0.99),
                    "expiry": (row.name + pd.Timedelta(days=7)).strftime("%Y-%m-%d"),
                    "entry_price": entry_price,
                    "exit_price": exit_price,
                    "return": exit_price - entry_price,
                    "side": "buy",
                    "confidence": confidence
                })

    return pd.DataFrame(trades)
def spy_momentum_strategy(data, config=None):
  """
  Live strategy returning ("buy"/"sell"/None, confidence)
  Filters weak setups (confidence < 4)
  """
  import numpy as np
  data = data.copy()
  data["EMA_9"] = data["Close"].ewm(span=9).mean()
  data["EMA_21"] = data["Close"].ewm(span=21).mean()
  data["RSI"] = compute_rsi(data["Close"])
  data["MACD"], _, hist = compute_macd(data["Close"])
  data["MACD_hist"] = hist
  data["Avg_Volume"] = data["Volume"].rolling(20).mean()

  row = data.iloc[-1]

  confidence = 0
  confidence += int(float(row["EMA_9"]) > float(row["EMA_21"]))
  confidence += int(float(row["RSI"]) > 50)
  confidence += int(float(row["MACD_hist"]) > 0)
  confidence += int(float(row["Volume"]) > float(row["Avg_Volume"]))

  if confidence < 4:
      return None, confidence  # 🚫 Weak setup — skip

  return "buy", confidence
