# test/test_webull_options.py

from data.webull_options import get_option_candidates

def test_scan():
    print("🔍 Scanning for high-IV SPY options...")
    options = get_option_candidates("SPY", min_iv=0.25, max_days=7)
    for opt in options[:5]:
        print(opt)

if __name__ == "__main__":
    test_scan()
