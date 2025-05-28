
def spy_momentum_strategy(df):
    """
    Returns 'buy', 'sell', or None based on simple moving average crossover.
    """
    if len(df) < 20:
        return None

    df["MA20"] = df["Close"].rolling(20).mean()
    current_price = df["Close"].iloc[-1]
    ma = df["MA20"].iloc[-1]

    if current_price > ma:
        return "buy"
    elif current_price < ma:
        return "sell"
    return None

