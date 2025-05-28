import json
from datetime import date, timedelta

def generate_option_configs():
    base = {
        "symbol": "SPY",
        "name": "SPY Option Momentum",
        "enabled": True,
        "type": "call",  # or "put"
        "quantity": 1,
        "target": 0.20,
        "stop": 0.10,
        "trailing_stop": 0.08,
        "breakeven_trigger": 0.12,
        "strike": 430,  # base strike
        "expiry": str(date.today() + timedelta(days=30))  # 1 month out
    }

    configs = []

    for opt_type in ["call", "put"]:
        for strike_offset in [-5, 0, 5]:  # 3 strikes
            config = base.copy()
            config["type"] = opt_type
            config["strike"] = base["strike"] + strike_offset
            config["name"] = f"{opt_type.upper()}-{config['strike']}"
            configs.append(config)

    with open("config/generated_options.json", "w") as f:
        json.dump({"strategies": configs}, f, indent=2)
        print(f"✅ Generated {len(configs)} option configs.")

if __name__ == "__main__":
    generate_option_configs()
