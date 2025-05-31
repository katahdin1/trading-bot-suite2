import importlib

def run_strategy(strategy_config):
    """
    Dynamically load and run the strategy defined in the config.
    The strategy must return (signal, confidence) tuple.
    """
    strategy_name = strategy_config["name"]
    module = importlib.import_module("backtest.strategy")
    strategy_func = getattr(module, strategy_name)

    # Load historical data
    from backtest.data import get_spy_data
    df = get_spy_data(interval="1d", range="7d")  # Short-term for live logic

    # Run strategy
    result = strategy_func(df, config=strategy_config)

    # Result must be a tuple (signal, confidence)
    if isinstance(result, tuple) and len(result) == 2:
        return result
    else:
        raise ValueError(f"{strategy_name} did not return (signal, confidence)")

