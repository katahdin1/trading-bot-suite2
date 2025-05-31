from reports.daily_report import send_daily_trade_report
from reports.weekly_report import send_weekly_summary

if __name__ == "__main__":
    print("📤 Sending test daily report...")
    send_daily_trade_report()

    print("📤 Sending test weekly summary...")
    send_weekly_summary()
summary_lines = []

for idx, trade in trades_df.iterrows():
    summary_lines.append(
        f"{trade['symbol']} {trade['action'].upper()} | Entry: {trade['entry_price']} | Exit: {trade.get('exit_price', 'N/A')} | Return: {trade.get('return', 'N/A')} | Confidence: {trade.get('confidence', 'N/A')}"
    )

summary_body = "\n".join(summary_lines)
full_body = f"📊 Daily Trade Report – {today}\n\n" + summary_body
