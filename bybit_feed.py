# bybit_feed.py
# Pulls live BTC/USDT market data from Bybit (REST API)

import requests
import pandas as pd

BYBIT_REST_URL = "https://api.bybit.com"

def fetch_bybit_klines(symbol="BTCUSDT", interval="1", limit=100):
    url = f"{BYBIT_REST_URL}/v5/market/kline"
    params = {
        "category": "linear",
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        raw = response.json().get("result", {}).get("list", [])
        return raw[::-1]  # reverse to get oldest first
    except Exception as e:
        print(f"[!] Error fetching Bybit klines: {e}")
        return []

def get_bybit_sniper_feed():
    raw = fetch_bybit_klines()
    if not raw:
        return None

    df = pd.DataFrame(raw, columns=[
        "timestamp", "open", "high", "low", "close", "volume", "turnover"
    ])

    df = df.astype(float)
    df["vwap"] = df["turnover"] / df["volume"]
    df["rsi"] = df["close"].rolling(window=14).apply(
        lambda x: 100 - (100 / (1 + (x.diff().clip(lower=0).mean() / abs(x.diff().clip(upper=0).mean())))) if x.count() >= 14 else 50
    )

    return df[["close", "vwap", "rsi", "volume"]].tail(20)
