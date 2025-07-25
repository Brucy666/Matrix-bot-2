# test_kucoin_timeframes.py

import requests
import time

KUCOIN_API_BASE = "https://api.kucoin.com"
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Test all known timeframe variants
TEST_INTERVALS = [
    "1min", "3min", "5min", "15min", "30min",
    "1hour", "2hour", "4hour", "6hour", "8hour",
    "12hour", "1day", "1week"
]

symbol = "BTC-USDT"
endpoint = f"{KUCOIN_API_BASE}/api/v1/market/candles"
start_time = int(time.time()) - (3600 * 24 * 2)  # last 2 days

print("\n🔍 Testing KuCoin supported timeframes...")

for interval in TEST_INTERVALS:
    params = {
        "type": interval,
        "symbol": symbol,
        "startAt": start_time
    }

    try:
        res = requests.get(endpoint, headers=HEADERS, params=params)
        data = res.json()

        if data.get("code") != "200000":
            print(f"❌ {interval} → Error: {data.get('msg')}")
        elif not data.get("data"):
            print(f"⚠️  {interval} → No usable data returned.")
        else:
            rows = len(data["data"])
            print(f"✅ {interval} → OK ({rows} rows)")

    except Exception as e:
        print(f"❌ {interval} → Exception: {e}")
