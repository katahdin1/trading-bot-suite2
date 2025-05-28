import yfinance as yf
import pandas as pd

def get_spy_data(period="6mo", interval="1d"):
    df = yf.download("SPY", period=period, interval=interval, auto_adjust=True)
    df = df.dropna()
    df.index.name = "Date"
    df.reset_index(inplace=True)
    return df
