# kucoin_feed.py

import requests
import pandas as pd
import os
import time

KUCOIN_API_BASE = "https://api.kucoin.com"

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Reliable KuCoin-supported timeframes
TIMEFRAMES = [
    ("1min", "1m"),
    ("5min", "5m"),
    ("15min", "15m"),
    ("1hour", "1h"),
    ("4hour", "4h")
]

def fetch_ohlcv(symbol: str, kucoin_tf: str):
    try:
        market = symbol.replace("/", "-").upper()  # BTC/USDT -> BTC-USDT
        endpoint = f"/api/v1/market/candles"
        params = {
            "type": kucoin_tf,
            "symbol": market,
            "startAt": int(time.time()) - 60 * 60 * 48  # last 48h
        }

        url = f"{KUCOIN_API_BASE}{endpoint}"
        response = requests.get(url, headers=HEADERS, params=params)
        data = response.json()

        if not data.get("data"):
            print(f"[KUCOIN ERROR] No data returned for {kucoin_tf}. Response: {data}")
            return None

        df = pd.DataFrame(data["data"], columns=[
            "timestamp", "open", "close", "high", "low", "volume", "turnover"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
        df = df.sort_values("timestamp")

        return df[["timestamp", "open", "high", "low", "close", "volume"]]

    except Exception as e:
        print(f"[KUCOIN ERROR] Failed to fetch OHLCV for {symbol} {kucoin_tf}: {e}")
        return None

def get_multi_tf_ohlcv(symbol: str):
    results = {}
    for kucoin_tf, label in TIMEFRAMES:
        print(f"[KUCOIN] ⏳ Fetching {label}...")
        df = fetch_ohlcv(symbol, kucoin_tf)
        if df is not None:
            results[label] = df
        else:
            print(f"[KUCOIN SKIP] {label} returned no usable data.")
    return results
