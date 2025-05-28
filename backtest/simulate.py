import os
import pandas as pd
from datetime import datetime

from backtest.data import get_spy_data
from backtest.strategy import (
    spy_momentum_strategy,
    spy_rsi_strategy,
    spy_options_strategy,
)
from backtest.metrics import evaluate_strategy
from utils.emailer import send_email_report
from utils.discord import send_discord

STRATEGIES = {
    "spy_momentum": spy_momentum_strategy,
    "spy_rsi": spy_rsi_strategy,
    "spy_options": spy_options_strategy,
}


def run_simulation():
    print("🧪 Running multi-strategy backtest...")
    df = get_spy_data(period="6mo", interval="1d")
    today = datetime.today().strftime("%Y-%m-%d")

    os.makedirs("logs", exist_ok=True)
    summary_lines = [f"📊 Backtest Report ({today})\n"]

    for name, strategy_func in STRATEGIES.items():
        print(f"\n🔎 Strategy: {name}")
        trades = strategy_func(df)
        results = evaluate_strategy(trades)

        # Save log
        csv_path = f"logs/{name}_trades_{today}.csv"
        trades.to_csv(csv_path, index=False)

        # Output summary
        summary = (
            f"📘 {name}:\n"
            f"  • Trades: {results['trades']}\n"
            f"  • Wins: {results['wins']}\n"
            f"  • Losses: {results['losses']}\n"
            f"  • Win Rate: {results['win_rate'] * 100:.2f}%\n"
            f"  • Net Profit: ${results['net_profit']:.2f}\n"
            f"  • Avg Return/Trade: ${results['avg_return_per_trade']:.2f}\n"
        )
        print(summary)
        summary_lines.append(summary)

    # Send email + Discord
    full_summary = "\n".join(summary_lines)
    send_email_report(
        subject=f"📊 Strategy Backtest Summary – {today}",
        body=full_summary,
        to_email=os.getenv("EMAIL_USER"),
        attachments=[
            f"logs/{name}_trades_{today}.csv" for name in STRATEGIES
        ],
    )
    send_discord(full_summary)


if __name__ == "__main__":
    run_simulation()
