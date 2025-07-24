# kucoin_feed.py (Option 1 - Clean & Stable)
import requests
import os
import time

API_KEY = os.getenv("KUCOIN_API_KEY")
BASE_URL = "https://api.kucoin.com"

HEADERS = {
    "KC-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

def fetch_ohlcv(symbol="BTC-USDT", interval="1min", limit=150):
    url = f"{BASE_URL}/api/v1/market/candles?type={interval}&symbol={symbol}&limit={limit}"
    try:
        res = requests.get(url)
        data = res.json()
        if data.get("code") != "200000":
            print(f"[KUCOIN ERROR] {data.get('msg')} ({interval})")
            return []
        return [
            {
                "timestamp": int(item[0]),
                "open": float(item[1]),
                "close": float(item[2]),
                "high": float(item[3]),
                "low": float(item[4]),
                "volume": float(item[5])
            }
            for item in data["data"]
        ]
    except Exception as e:
        print(f"[KUCOIN ERROR] {e} ({interval})")
        return []

def get_multi_tf_ohlcv(symbol="BTC-USDT"):
    timeframes = ["1min", "5min", "15min", "1hour", "4hour"]
    tf_data = {}
    for tf in timeframes:
        print(f"[KUCOIN FEED] Fetching {tf} data...")
        candles = fetch_ohlcv(symbol, tf)
        if candles:
            tf_data[tf] = candles
        else:
            print(f"[KUCOIN FEED] No data for {tf}")
        time.sleep(0.4)  # KuCoin allows 15 req/sec burst, but this is safe
    return tf_data

if __name__ == "__main__":
    result = get_multi_tf_ohlcv("BTC-USDT")
    for tf, data in result.items():
        print(f"✅ {tf} => {len(data)} candles")
