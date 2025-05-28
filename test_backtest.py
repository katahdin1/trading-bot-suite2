from backtest.simulate import run_simulation

if __name__ == "__main__":
    print("🧪 Running full bot backtest...")
    results = run_simulation()

    print("📊 Backtest Metrics:")
    for k, v in results.items():
        print(f"{k}: {v}")
from backtest.simulate import run_simulation

run_simulation()
