import yfinance as yf
import pandas as pd

def get_spy_data(start="2022-01-01", end="2024-12-31"):
    df = yf.download("SPY", start=start, end=end)
    df = df[["Close"]].rename(columns={"Close": "price"})
    df["ma_50"] = df["price"].rolling(50).mean()
    df.dropna(inplace=True)
    return df

