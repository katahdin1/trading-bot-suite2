from backtest.data import get_spy_data
from strategy import generate_signals
from metrics import calculate_pnl
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.emailer import send_email_report
import os

RISK_PER_TRADE = 500
STOP_LOSS = 0.10  # -10%
TARGET = 0.30     # +30%

def run_simulation():
    df = get_spy_data()
    df = generate_signals(df)

    trades = []

    for i in range(len(df)):
        row = df.iloc[i]
        if row['signal'] in ['call', 'put']:
            direction = row['signal']
            entry_price = row['Close']
            trade_outcome = None
            pnl = 0

            for j in range(i + 1, min(i + 12, len(df))):  # look ahead 1 hour
                future_price = df.iloc[j]['Close']
                move = (future_price - entry_price) / entry_price if direction == 'call' else (entry_price - future_price) / entry_price

                if move >= TARGET:
                    trade_outcome = 'win'
                    pnl = RISK_PER_TRADE * TARGET
                    break
                elif move <= STOP_LOSS:
                    trade_outcome = 'loss'
                    pnl = -RISK_PER_TRADE * STOP_LOSS
                    break

            if trade_outcome:
                trades.append({
                    'time': df.index[i],
                    'signal': direction,
                    'entry': round(entry_price, 2),
                    'result': trade_outcome,
                    'pnl': pnl
                })

    df_trades = pd.DataFrame(trades)
    df_trades.to_csv("simulated_trades.csv", index=False)

    stats = calculate_pnl(trades)
    print("📊 Simulation Results:")
    print(stats)

    send_email_report(
        subject="📊 SPY Simulation Report",
        body="Attached is the simulated trade log from your backtest.",
        to_email=os.getenv("EMAIL_USER"),
        attachments=["simulated_trades.csv"]
    )

if __name__ == "__main__":
    run_simulation()
from backtest.data import get_spy_data
from backtest.strategy import spy_momentum_strategy
from backtest.metrics import evaluate_strategy
from utils.emailer import send_email_report

def run_simulation():
    df = get_spy_data()
    trades = spy_momentum_strategy(df)
    results = evaluate_strategy(trades)

    print("📊 Simulation Results:")
    print(results)

    # Optional: Email PDF or text summary
    send_email_report(
        subject="🧪 Backtest Summary",
        body=str(results),
        to_email="kysenick@gmail.com"
    )

if __name__ == "__main__":
    run_simulation()
