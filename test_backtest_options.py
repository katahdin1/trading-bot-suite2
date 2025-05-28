from backtest.simulate import run_simulation
import json

with open("config/generated_options.json") as f:
    config = json.load(f)

for strat in config["strategies"]:
    print(f"\n🔁 Backtesting: {strat['name']}")

    run_simulation(
        symbol=strat["symbol"],
        option_type=strat["type"],
        strike=strat["strike"],
        expiry=strat["expiry"],
        target=strat["target"],
        stop=strat["stop"],
        trailing_stop=strat.get("trailing_stop"),
        breakeven_trigger=strat.get("breakeven_trigger"),
        show_summary=True
    )
