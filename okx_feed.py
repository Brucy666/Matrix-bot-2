# okx_feed.py
# ✅ OKX Feed Module: OHLCV + Orderbook for BTC Sniper Engine

import requests
import pandas as pd

BASE_URL = "https://www.okx.com"
HEADERS = {"Accept": "application/json"}

# ----------------------------------------
# ✅ Safe OHLCV Fetcher
# ----------------------------------------
def get_okx_ohlcv(symbol="BTC-USDT", interval="1m", limit=100):
    url = f"{BASE_URL}/api/v5/market/candles"
    params = {
        "instId": symbol,
        "bar": interval,
        "limit": limit
    }

    try:
        res = requests.get(url, headers=HEADERS, params=params, timeout=5)
        res.raise_for_status()
        raw = res.json().get("data", [])

        if not raw or len(raw) == 0:
            print("[OKX FEED] ⚠️ No OHLCV data returned.")
            return None

        # Convert to DataFrame
        df = pd.DataFrame(raw[::-1], columns=[
            "ts", "open", "high", "low", "close", "volume", "volCcy", "volCcyQuote"
        ])
        df["timestamp"] = pd.to_datetime(df["ts"].astype(float), unit="ms")
        df["close"] = df["close"].astype(float)
        df["volume"] = df["volume"].astype(float)

        print(f"[OKX FEED] ✅ OHLCV rows: {len(df)}")
        return df

    except Exception as e:
        print("[OKX FEED ERROR]", e)
        return None

# ----------------------------------------
# ✅ Order Book Snapshot
# ----------------------------------------
def fetch_okx_orderbook(symbol="BTC-USDT", depth=40):
    url = f"{BASE_URL}/api/v5/market/books"
    params = {
        "instId": symbol,
        "sz": depth
    }

    try:
        res = requests.get(url, headers=HEADERS, params=params, timeout=5)
        res.raise_for_status()
        data = res.json().get("data", [])

        if not data or "bids" not in data[0] or "asks" not in data[0]:
            print("[OKX OB] ⚠️ Incomplete order book returned.")
            return [], []

        bids = [(float(p), float(q)) for p, q, *_ in data[0]["bids"]]
        asks = [(float(p), float(q)) for p, q, *_ in data[0]["asks"]]

        print(f"[OKX OB] ✅ Bids: {len(bids)} | Asks: {len(asks)}")
        return bids, asks

    except Exception as e:
        print("[OKX OB ERROR]", e)
        return [], []

# ----------------------------------------
# 🔧 Test Mode
# ----------------------------------------
if __name__ == "__main__":
    df = get_okx_ohlcv()
    if df is not None:
        print(df[["timestamp", "close", "volume"]].tail())

    bids, asks = fetch_okx_orderbook()
    if bids and asks:
        print("Top Bid:", bids[0], "Top Ask:", asks[0])
