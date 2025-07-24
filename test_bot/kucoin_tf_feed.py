# kucoin_tf_feed.py
# Fetches multi-timeframe OHLCV data from KuCoin for Echo V engine

import requests
import pandas as pd
import time
import os

API_KEY = os.getenv("KUCOIN_API_KEY")
SYMBOL = "BTC-USDT"

# Timeframe map (KuCoin -> interval in seconds)
TF_INTERVALS = {
    "4h": 14400,
    "1h": 3600,
    "15m": 900,
    "5m": 300
}

# Max candles to fetch per timeframe (keep small for test bot)
CANDLES_LIMIT = 50

BASE_URL = "https://api.kucoin.com"

def get_klines(symbol: str, interval: int, limit: int):
    url = f"{BASE_URL}/api/v1/market/candles"
    params = {
        "type": str(interval),
        "symbol": symbol,
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if data.get("code") != "200000":
            raise Exception(f"Invalid response code: {data.get('code')}")
        raw = data.get("data", [])[:limit]
        df = pd.DataFrame(raw, columns=[
            "timestamp", "open", "close", "high", "low", "volume", "turnover"])
        df = df.astype(float)
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
        df = df.sort_values("timestamp")
        return df
    except Exception as e:
        print(f"[KUCOIN FEED ERROR] {e}")
        return pd.DataFrame()

def get_multi_tf_ohlcv():
    tf_data = {}
    for tf, seconds in TF_INTERVALS.items():
        print(f"[TF FEED] Fetching {tf}...")
        df = get_klines(SYMBOL, seconds, CANDLES_LIMIT)
        if not df.empty:
            tf_data[tf] = df
    return tf_data
