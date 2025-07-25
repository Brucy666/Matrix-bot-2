# test_kucoin_feed.py

import requests
import pandas as pd

KUCOIN_API_BASE = "https://api.kucoin.com"
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

TIMEFRAMES = {
    "1min": "1min",
    "5min": "5min",
    "15min": "15min",
    "1hour": "1hour",
    "4hour": "4hour"
}

def fetch_ohlcv(symbol="BTC-USDT", tf="1min"):
    try:
        url = f"{KUCOIN_API_BASE}/api/v1/market/candles"
        params = {
            "symbol": symbol,
            "type": tf,
            "startAt": int(pd.Timestamp.utcnow().timestamp()) - 3600 * 12
        }
        res = requests.get(url, headers=HEADERS, params=params).json()
        data = res.get("data", [])
        print(f"[{tf}] ✅ {len(data)} candles returned" if data else f"[{tf}] ❌ No data")
    except Exception as e:
        print(f"[{tf}] ❌ Error: {e}")

if __name__ == "__main__":
    for tf in TIMEFRAMES.values():
        fetch_ohlcv(tf=tf)
