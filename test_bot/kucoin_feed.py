# kucoin_feed.py
# Fetches OHLCV data from KuCoin for multiple timeframes

import os
import requests
import pandas as pd
from datetime import datetime

BASE_URL = "https://api.kucoin.com"
SYMBOL = "BTC-USDT"
TIMEFRAMES = ["1min", "5min", "15min", "1hour", "4hour"]
LIMIT = 150  # Number of candles

def fetch_ohlcv(symbol=SYMBOL, interval="1min", limit=LIMIT):
    try:
        url = f"{BASE_URL}/api/v1/market/candles?type={interval}&symbol={symbol}&limit={limit}"
        response = requests.get(url)
        raw = response.json()

        if "data" not in raw or not isinstance(raw["data"], list) or len(raw["data"]) == 0:
            print(f"[KUCOIN ERROR] No data returned for {interval}. Response: {raw}")
            return None

        df = pd.DataFrame(raw["data"], columns=[
            "timestamp", "open", "close", "high", "low", "volume", "turnover"
        ])

        df = df[::-1].copy()  # Reverse to chronological
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", errors="coerce")
        df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)
        df = df.dropna(subset=["timestamp"])
        df.reset_index(drop=True, inplace=True)

        return df

    except Exception as e:
        print(f"[KUCOIN ERROR] Exception during fetch for {interval}: {e}")
        return None

def get_multi_ohlcv(symbol=SYMBOL, timeframes=TIMEFRAMES):
    tf_data = {}

    for tf in timeframes:
        df = fetch_ohlcv(symbol, tf)
        if df is not None and len(df) >= 50:
            tf_data[tf] = df
        else:
            print(f"[KUCOIN ERROR] Skipped {tf} due to insufficient or missing data.")

    return tf_data
