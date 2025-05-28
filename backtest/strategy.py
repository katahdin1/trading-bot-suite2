import pandas as pd

def apply_indicators(df):
    df['EMA20'] = df['Close'].ewm(span=20).mean()
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = -delta.where(delta < 0, 0).rolling(14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

def generate_signals(df):
    df = apply_indicators(df)
    df['signal'] = None

    for i in range(1, len(df)):
        if df['Close'].iloc[i] > df['EMA20'].iloc[i] and df['RSI'].iloc[i] > 55:
            df.at[df.index[i], 'signal'] = 'call'
        elif df['Close'].iloc[i] < df['EMA20'].iloc[i] and df['RSI'].iloc[i] < 45:
            df.at[df.index[i], 'signal'] = 'put'
    return df
