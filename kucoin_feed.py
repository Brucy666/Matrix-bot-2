# kucoin_feed.py
import requests
import pandas as pd

KCS_BASE_URL = "https://api.kucoin.com"

def fetch_klines(symbol="BTC-USDT", interval="1min", limit=100):
    url = f"{KCS_BASE_URL}/api/v1/market/candles"
    params = {"symbol": symbol, "type": interval}
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json().get("data", [])[:limit]
    except Exception as e:
        print(f"[!] Error fetching klines: {e}")
        return []

def fetch_orderbook(symbol="BTC-USDT"):
    url = f"{KCS_BASE_URL}/api/v1/market/orderbook/level2_20"
    params = {"symbol": symbol}
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json().get("data", {})
        bids = data.get("bids", [])
        asks = data.get("asks", [])
        total_bids = sum(float(b[1]) for b in bids)
        total_asks = sum(float(a[1]) for a in asks)
        return {"bids": total_bids, "asks": total_asks}
    except Exception as e:
        print(f"[!] Error fetching orderbook: {e}")
        return {"bids": 1.0, "asks": 1.0}

# ✅ Sniper-ready feed function
def get_kucoin_sniper_feed():
    raw = fetch_klines()
    if not raw or len(raw[0]) < 7:
        return None

    # Transform into DataFrame
    df = pd.DataFrame(raw, columns=[
        "timestamp", "open", "close", "high", "low", "volume", "turnover"
    ])

    df = df.astype(float)
    df["vwap"] = df["turnover"] / df["volume"]
    df["rsi"] = df["close"].rolling(window=14).apply(lambda x: 100 - (100 / (1 + (x.diff().clip(lower=0).mean() / abs(x.diff().clip(upper=0).mean())))) if x.count() >= 14 else 50)

    return df[["close", "vwap", "rsi", "volume"]].tail(20)
