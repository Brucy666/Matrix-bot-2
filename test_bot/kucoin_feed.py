# kucoin_feed.py

import requests
import pandas as pd

KUCOIN_API_BASE = "https://api.kucoin.com"
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Try all common timeframes for testing
TEST_TIMEFRAMES = ["1min", "3min", "5min", "15min", "30min", "1hour", "2hour", "4hour", "6hour", "8hour", "12hour", "1day"]


def fetch_ohlcv(symbol: str, kucoin_tf: str):
    try:
        market = symbol.replace("/", "-").upper()  # e.g., BTC/USDT -> BTC-USDT
        endpoint = "/api/v1/market/candles"
        params = {
            "type": kucoin_tf,
            "symbol": market,
            "startAt": int(pd.Timestamp.utcnow().timestamp()) - 3600 * 24 * 2  # 2 days ago
        }

        url = f"{KUCOIN_API_BASE}{endpoint}"
        response = requests.get(url, headers=HEADERS, params=params)
        data = response.json()

        if not data.get("data"):
            print(f"[KUCOIN ❌] {kucoin_tf} returned no usable data.")
            return False

        print(f"[KUCOIN ✅] {kucoin_tf} returned {len(data['data'])} candles.")
        return True

    except Exception as e:
        print(f"[KUCOIN ERROR] {kucoin_tf} failed: {e}")
        return False


if __name__ == "__main__":
    print("\n[KUCOIN TESTER] Checking supported timeframes for BTC/USDT\n")
    for tf in TEST_TIMEFRAMES:
        fetch_ohlcv("BTC/USDT", tf)
