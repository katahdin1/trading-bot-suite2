import pandas as pd
from backtest.data import get_spy_data
from backtest.strategy import spy_rsi_strategy
from backtest.metrics import evaluate_strategy

def grid_search_rsi(thresholds=[30, 35, 40], profit_targets=[1.03, 1.05]):
    df = get_spy_data(interval="1d", range="6mo")
    results = []

    for rsi_thresh in thresholds:
        for pt in profit_targets:
            trades = spy_rsi_strategy(df, entry_rsi=rsi_thresh, profit_target=pt)
            metrics = evaluate_strategy(trades)
            metrics.update({
                "entry_rsi": rsi_thresh,
                "profit_target": pt,
                "trades": len(trades)
            })
            results.append(metrics)

    return pd.DataFrame(results)

if __name__ == "__main__":
    df = grid_search_rsi()
    print(df.sort_values(by="net_profit", ascending=False).head(10))
import os
import pandas as pd
from datetime import datetime
from backtest.data import get_spy_data
from backtest.strategy import spy_rsi_strategy
from backtest.metrics import evaluate_strategy
from utils.emailer import send_email_report
from utils.discord import send_discord

def grid_search_rsi(entry_rsi_vals, profit_targets):
    df = get_spy_data(interval="1d", range="6mo")
    results = []

    for rsi_thresh in entry_rsi_vals:
        for pt in profit_targets:
            trades = spy_rsi_strategy(df, entry_rsi=rsi_thresh, profit_target=pt)
            metrics = evaluate_strategy(trades)
            metrics.update({
                "entry_rsi": rsi_thresh,
                "profit_target": pt,
                "trades": len(trades)
            })
            results.append(metrics)

    return pd.DataFrame(results)

if __name__ == "__main__":
    print("📊 Running RSI Grid Search...")
    df = grid_search_rsi(entry_rsi_vals=[25, 30, 35], profit_targets=[1.03, 1.05, 1.07])

    today = datetime.today().strftime("%Y-%m-%d")
    os.makedirs("reports", exist_ok=True)
    output_csv = f"reports/rsi_grid_{today}.csv"
    df.to_csv(output_csv, index=False)

    best = df.sort_values(by="net_profit", ascending=False).iloc[0]

    summary = (
        f"📈 Best RSI Strategy ({today})\n\n"
        f"RSI Entry: {best['entry_rsi']}\n"
        f"Profit Target: {best['profit_target']}\n"
        f"Trades: {best['trades']}\n"
        f"Win Rate: {best['win_rate']*100:.1f}%\n"
        f"Net Profit: ${best['net_profit']:.2f}"
    )

    send_email_report(
        subject=f"RSI Grid Search – {today}",
        body=summary,
        to_email=os.getenv("EMAIL_USER"),
        attachments=[output_csv]
    )

    send_discord(summary)
    print("✅ Report sent.")
