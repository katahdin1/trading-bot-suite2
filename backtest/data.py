import yfinance as yf
import pandas as pd

def get_spy_data(period="6mo", interval="1d"):
    df = yf.download("SPY", period=period, interval=interval, auto_adjust=True)
    df = df.dropna()
    df.index.name = "Date"
    df.reset_index(inplace=True)
    return df
import yfinance as yf

def get_spy_data(symbol="SPY", interval="1d", range="6mo"):
    df = yf.download(symbol, interval=interval, period=range)
    return df.reset_index()
df = get_spy_data(symbol="QQQ", interval="1h", range="1mo")
