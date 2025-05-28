import pandas as pd
import numpy as np

def evaluate_strategy(trades: pd.DataFrame) -> dict:
    if trades.empty or "return" not in trades.columns:
        return {
            "trades": 0,
            "wins": 0,
            "losses": 0,
            "win_rate": 0.0,
            "net_profit": 0.0,
            "avg_return_per_trade": 0.0,
            "max_drawdown": 0.0,
            "sharpe_ratio": 0.0,
        }

    returns = trades["return"]
    trades["cumulative"] = returns.cumsum()

    wins = (returns > 0).sum()
    losses = (returns <= 0).sum()
    net_profit = returns.sum()
    avg_return = returns.mean()

    win_rate = wins / len(trades)

    # Max Drawdown Calculation
    cumulative = trades["cumulative"]
    rolling_max = cumulative.cummax()
    drawdown = cumulative - rolling_max
    max_drawdown = drawdown.min()

    # Sharpe Ratio (daily)
    sharpe = (
        (returns.mean() / returns.std()) * np.sqrt(252)
        if returns.std() != 0 else 0.0
    )

    return {
        "trades": len(trades),
        "wins": wins,
        "losses": losses,
        "win_rate": round(win_rate, 4),
        "net_profit": round(net_profit, 2),
        "avg_return_per_trade": round(avg_return, 2),
        "max_drawdown": round(max_drawdown, 2),
        "sharpe_ratio": round(sharpe, 2),
    }
import pandas as pd
import numpy as np

def evaluate_strategy(trades: pd.DataFrame) -> dict:
    if trades.empty or "return" not in trades.columns:
        return {
            "trades": 0,
            "wins": 0,
            "losses": 0,
            "win_rate": 0.0,
            "net_profit": 0.0,
            "avg_return_per_trade": 0.0,
            "max_drawdown": 0.0,
            "sharpe_ratio": 0.0,
        }

    returns = trades["return"]
    trades["cumulative"] = returns.cumsum()

    wins = (returns > 0).sum()
    losses = (returns <= 0).sum()
    net_profit = returns.sum()
    avg_return = returns.mean()

    win_rate = wins / len(trades)

    # Max Drawdown Calculation
    cumulative = trades["cumulative"]
    rolling_max = cumulative.cummax()
    drawdown = cumulative - rolling_max
    max_drawdown = drawdown.min()

    # Sharpe Ratio (daily)
    sharpe = (
        (returns.mean() / returns.std()) * np.sqrt(252)
        if returns.std() != 0 else 0.0
    )

    return {
        "trades": len(trades),
        "wins": wins,
        "losses": losses,
        "win_rate": round(win_rate, 4),
        "net_profit": round(net_profit, 2),
        "avg_return_per_trade": round(avg_return, 2),
        "max_drawdown": round(max_drawdown, 2),
        "sharpe_ratio": round(sharpe, 2),
    }
import pandas as pd

def evaluate_strategy(data: pd.DataFrame):
    """
    Evaluate performance: win rate, profit, etc.
    Automatically calculates return if not present.
    """
    if "return" not in data.columns:
        if {"entry_price", "exit_price"}.issubset(data.columns):
            data["return"] = data["exit_price"] - data["entry_price"]

    wins = (data["return"] > 0).sum()
    losses = (data["return"] <= 0).sum()
    total_trades = wins + losses
    net_profit = data["return"].sum()
    avg_return = data["return"].mean() if total_trades > 0 else 0

    return {
        "trades": total_trades,
        "wins": wins,
        "losses": losses,
        "win_rate": wins / total_trades if total_trades > 0 else 0,
        "net_profit": net_profit,
        "avg_return_per_trade": avg_return
    }
