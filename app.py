# app.py
import streamlit as st
import threading
import time
import json
import os

from main import run_bot, load_config
from reports.daily_report import send_daily_trade_report
from reports.weekly_report import send_weekly_summary

# === Streamlit Persistent State ===
if "bot_running" not in st.session_state:
    st.session_state.bot_running = False

st.title("🤖 Trade Bot Dashboard")

# === Sidebar Configuration ===
st.sidebar.header("⚙️ Bot Settings")

# Strategy selection
strategy_options = ["spy_rsi", "spy_momentum", "spy_options"]
selected_strategy = st.sidebar.selectbox("Select Strategy", strategy_options)

# Trading mode
mode = st.sidebar.selectbox("Trading Mode", ["paper", "options", "live"])

# Confidence filter
strict_confidence = st.sidebar.checkbox("🧠 Strict Mode: Confidence ≥ 4", value=True)

# Run interval (seconds)
interval = st.sidebar.slider("Run every N seconds", min_value=30, max_value=300, step=30, value=60)

# === BOT THREAD ===
def bot_loop():
    while st.session_state.bot_running:
        config = load_config()
        config["mode"] = mode
        for strat in config["strategies"]:
            strat["enabled"] = (strat["name"] == selected_strategy)
        with open("config/config.json", "w") as f:
            json.dump(config, f, indent=2)
        run_bot(live_mode=mode, strategy_key=selected_strategy, strict=strict_confidence)
        time.sleep(interval)

# === ACTION BUTTONS ===
if st.button("🚀 Start Bot", disabled=st.session_state.bot_running):
    st.session_state.bot_running = True
    threading.Thread(target=bot_loop, daemon=True).start()
    st.success("✅ Bot started")

if st.button("🛑 Stop Bot", disabled=not st.session_state.bot_running):
    st.session_state.bot_running = False
    st.warning("🛑 Bot stopped")

# === Reports ===
st.sidebar.header("📊 Manual Reports")

if st.sidebar.button("📩 Send Daily Report"):
    send_daily_trade_report()
    st.sidebar.success("✅ Daily report sent")

if st.sidebar.button("🗓 Send Weekly Summary"):
    send_weekly_summary()
    st.sidebar.success("✅ Weekly summary sent")

# === Trade Log Viewer ===
st.subheader("📜 Recent Trades")

log_file = f"logs/trades_{time.strftime('%Y-%m-%d')}.csv"
if os.path.exists(log_file):
    import pandas as pd
    df = pd.read_csv(log_file)
    st.dataframe(df.tail(10))
else:
    st.info("No trades logged today.")
