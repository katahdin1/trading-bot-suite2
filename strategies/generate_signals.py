# strategy/generate_signals.py

import pandas as pd

def generate_signals(data: pd.DataFrame, config: dict) -> str:
    """
    Generate buy/sell/hold signal based on a simple moving average crossover strategy.

    Args:
        data (pd.DataFrame): Historical OHLCV data.
        config (dict): Strategy configuration, expects keys like 'short_window', 'long_window'.

    Returns:
        str: "buy", "sell", or "hold"
    """
    short_window = config.get("short_window", 10)
    long_window = config.get("long_window", 50)

    # Calculate moving averages
    data["SMA_Short"] = data["Close"].rolling(window=short_window).mean()
    data["SMA_Long"] = data["Close"].rolling(window=long_window).mean()

    # Ensure enough data to generate signals
    if data[["SMA_Short", "SMA_Long"]].isnull().values.any():
        return "hold"

    # Get latest values
    latest_short = data["SMA_Short"].iloc[-1]
    latest_long = data["SMA_Long"].iloc[-1]

    if latest_short > latest_long:
        return "buy"
    elif latest_short < latest_long:
        return "sell"
    else:
        return "hold"
