# okx_feed.py
# Pulls OHLCV and order book data from OKX

import requests
import pandas as pd

BASE_URL = "https://www.okx.com"
HEADERS = {"Accept": "application/json"}

# ✅ OHLCV fetcher (updated to support 9 columns)
def get_okx_ohlcv(symbol="BTC-USDT", interval="1m", limit=100):
    url = f"{BASE_URL}/api/v5/market/candles"
    params = {
        "instId": symbol,
        "bar": interval,
        "limit": limit
    }

    try:
        res = requests.get(url, headers=HEADERS, params=params)
        res.raise_for_status()
        data = res.json().get("data", [])

        # OKX now returns 9 columns; map accordingly
        df = pd.DataFrame(data[::-1], columns=[
            "ts", "open", "high", "low", "close", "volume", "volumeCcy", "volumeCcyQuote", "confirm"
        ])
        df["timestamp"] = pd.to_datetime(df["ts"].astype(float), unit="ms")
        df["close"] = df["close"].astype(float)
        df["volume"] = df["volume"].astype(float)
        return df
    except Exception as e:
        print("[OKX ERROR]", e)
        return None

# ✅ Order book fetcher
def fetch_okx_orderbook(symbol="BTC-USDT", depth=40):
    url = f"{BASE_URL}/api/v5/market/books"
    params = {
        "instId": symbol,
        "sz": depth
    }

    try:
        res = requests.get(url, headers=HEADERS, params=params)
        res.raise_for_status()
        data = res.json().get("data", [])[0]

        bids = [(float(p), float(q)) for p, q, *_ in data["bids"]]
        asks = [(float(p), float(q)) for p, q, *_ in data["asks"]]
        return bids, asks
    except Exception as e:
        print("[OKX OB ERROR]", e)
        return [], []

# 🔧 Example test
if __name__ == "__main__":
    df = get_okx_ohlcv()
    print(df.tail())

    bids, asks = fetch_okx_orderbook()
    print("Top Bid:", bids[0] if bids else "N/A", "Top Ask:", asks[0] if asks else "N/A")
