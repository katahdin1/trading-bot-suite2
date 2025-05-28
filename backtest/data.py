import yfinance as yf
import pandas as pd

def get_spy_data(interval='5m', period='60d'):
    spy = yf.Ticker("SPY")
    df = spy.history(interval=interval, period=period)
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
    df.dropna(inplace=True)
    df.index = pd.to_datetime(df.index)
    return df
