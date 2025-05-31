import os
import pandas as pd
from datetime import datetime
from backtest.data import get_spy_data
from backtest.strategy import strategy_lookup
from backtest.metrics import evaluate_strategy
from utils.emailer import send_email_report
from utils.discord import send_discord

def run_simulation():
    print("🧪 Running multi-strategy backtest...\n")

    df = get_spy_data("6mo", "1d")  # Adjust if using a different loader

    all_results = []

    for name, strategy_func in strategy_lookup.items():
        print(f"🔎 Strategy: {name}")
        trades = strategy_func(df)

        if trades.empty:
            print("⚠️ No trades found.\n")
            continue

        results = evaluate_strategy(trades)
        all_results.append((name, results))

        # Save per-strategy logs
        today = datetime.today().strftime("%Y-%m-%d")
        os.makedirs("logs", exist_ok=True)
        csv_path = f"logs/{name}_trades_{today}.csv"
        trades.to_csv(csv_path, index=False)

        # Prepare summary
        summary = (
            f"📊 Backtest Report – {name} ({today})\n"
            f"Trades: {results['trades']}\n"
            f"Wins: {results['wins']}\n"
            f"Losses: {results['losses']}\n"
            f"Win Rate: {results['win_rate'] * 100:.2f}%\n"
            f"Net Profit: ${results['net_profit']:.2f}\n"
            f"Avg Return/Trade: ${results['avg_return_per_trade']:.2f}"
        )

        print(summary + "\n")

        # Send report
        send_email_report(
            subject=f"{name.upper()} Backtest Results – {today}",
            body=summary,
            attachments=[csv_path],
            to_email=os.getenv("EMAIL_USER")
        )

        send_discord(summary)

    return all_results

if __name__ == "__main__":
    run_simulation()
