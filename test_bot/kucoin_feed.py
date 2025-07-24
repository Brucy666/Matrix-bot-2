# test_bot/kucoin_feed.py

import requests
import pandas as pd
import time
import os

KUCOIN_API_KEY = os.getenv("KUCOIN_API_KEY")
SYMBOL = "BTC-USDT"

def fetch_klines(symbol, interval, limit=150):
    url = f"https://api.kucoin.com/api/v1/market/candles?type={interval}&symbol={symbol}&limit={limit}"
    headers = {"KC-API-KEY": KUCOIN_API_KEY} if KUCOIN_API_KEY else {}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()
        if data.get("code") != "200000":
            print(f"[KUCOIN ERROR] Response code: {data.get('code')}")
            return None
        rows = data["data"]
        df = pd.DataFrame(rows, columns=[
            "timestamp", "open", "close", "high", "low", "volume", "turnover"
        ])
        df = df.iloc[::-1]  # Reverse order: oldest → newest
        df["timestamp"] = pd.to_numeric(df["timestamp"], errors="coerce")
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)
        return df
    except Exception as e:
        print(f"[KUCOIN ERROR] API error: {e}")
        return None

def get_multi_tf_kucoin_data():
    timeframes = {
        "1m": "1min",
        "5m": "5min",
        "15m": "15min",
        "1h": "1hour",
        "4h": "4hour"
    }
    data_map = {}
    for label, interval in timeframes.items():
        df = fetch_klines(SYMBOL, interval)
        if df is not None and len(df) > 20:
            data_map[label] = df
    return data_map
