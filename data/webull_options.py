# data/webull_options.py

def get_option_candidates(symbol="SPY", min_iv=0.25, max_days=7):
    # Simulated options data (you'll replace this later with real API calls)
    return [
        {"symbol": symbol, "type": "call", "strike": 430, "expiry": "2025-06-21", "iv": 0.35},
        {"symbol": symbol, "type": "put", "strike": 420, "expiry": "2025-06-14", "iv": 0.32},
        {"symbol": symbol, "type": "call", "strike": 435, "expiry": "2025-06-28", "iv": 0.45},
        {"symbol": symbol, "type": "put", "strike": 410, "expiry": "2025-06-21", "iv": 0.28},
        {"symbol": symbol, "type": "call", "strike": 440, "expiry": "2025-06-07", "iv": 0.3}
    ]
