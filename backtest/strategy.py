import pandas as pd
import ta  # Make sure `ta` is installed: pip install ta

# === Helper Functions ===

def compute_rsi(series, window=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def compute_macd(close):
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    macd_line = ema12 - ema26
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    macd_hist = macd_line - signal_line
    return macd_line, signal_line, macd_hist

# === Strategy 1: SPY Momentum ===

def spy_momentum_strategy(data):
    data = data.copy()
    data["EMA_9"] = data["Close"].ewm(span=9, adjust=False).mean()
    data["EMA_21"] = data["Close"].ewm(span=21, adjust=False).mean()
    data["RSI"] = compute_rsi(data["Close"])
    data["MACD_line"], data["Signal_line"], data["MACD_hist"] = compute_macd(data["Close"])
    data["Avg_Volume"] = data["Volume"].rolling(window=20).mean()

    trades = []
    position = None
    trailing_stop_pct = 0.02

    for i in range(1, len(data)):
        row = data.iloc[i]

        confidence = 0
        confidence += int(row["EMA_9"] > row["EMA_21"])
        confidence += int(row["RSI"] > 55)
        confidence += int(row["MACD_hist"] > 0)
        confidence += int(row["Volume"] > row["Avg_Volume"])

        if position is None and confidence >= 3:
            entry_price = row["Close"]
            position = {
                "entry_date": row.name,
                "entry_price": entry_price,
                "trail_price": entry_price,
                "take_profit": entry_price * 1.02
            }

        elif position:
            if row["Close"] > position["trail_price"]:
                position["trail_price"] = row["Close"]

            trail_stop = position["trail_price"] * (1 - trailing_stop_pct)

            if row["Close"] <= trail_stop or row["Close"] >= position["take_profit"]:
                trades.append({
                    "entry_date": position["entry_date"],
                    "exit_date": row.name,
                    "entry_price": position["entry_price"],
                    "exit_price": row["Close"],
                    "return": row["Close"] - position["entry_price"]
                })
                position = None

    return pd.DataFrame(trades)

# === Strategy 2: RSI Mean Reversion ===

def spy_rsi_strategy(data):
    data = data.copy()
    data["RSI"] = compute_rsi(data["Close"], window=14)

    trades = []
    position = None

    for i in range(1, len(data)):
        row = data.iloc[i]
        prev = data.iloc[i - 1]

        if position is None and prev["RSI"] < 30 and row["RSI"] > 30:
            entry = row["Close"]
            trades.append({
                "date": row.name,
                "side": "buy",
                "entry_price": entry,
                "exit_price": entry * 1.03,
                "return": entry * 0.03
            })
            position = "entered"

        elif position and row["RSI"] > 70:
            position = None

    return pd.DataFrame(trades)

# === Strategy 3: Options MA Breakout ===

def spy_options_strategy(data):
    data = data.copy()
    data["MA_20"] = data["Close"].rolling(window=20).mean()

    trades = []

    for i in range(1, len(data)):
        row = data.iloc[i]
        prev = data.iloc[i - 1]

        if prev["Close"] < prev["MA_20"] and row["Close"] > row["MA_20"]:
            # Bullish breakout → Call Option
            trades.append({
                "date": row.name,
                "symbol": "SPY",
                "type": "call",
                "strike": round(row["Close"] * 1.01),
                "expiry": (row.name + pd.Timedelta(days=7)).strftime("%Y-%m-%d"),
                "entry_price": 2.50,
                "exit_price": 3.00,
                "return": 0.50,
                "side": "buy"
            })

        elif prev["Close"] > prev["MA_20"] and row["Close"] < row["MA_20"]:
            # Bearish breakdown → Put Option
            trades.append({
                "date": row.name,
                "symbol": "SPY",
                "type": "put",
                "strike": round(row["Close"] * 0.99),
                "expiry": (row.name + pd.Timedelta(days=7)).strftime("%Y-%m-%d"),
                "entry_price": 2.50,
                "exit_price": 3.00,
                "return": 0.50,
                "side": "buy"
            })

    return pd.DataFrame(trades)

# === Strategy Lookup ===

strategy_lookup = {
    "spy_momentum": spy_momentum_strategy,
    "spy_rsi": spy_rsi_strategy,
    "spy_options": spy_options_strategy,
}
