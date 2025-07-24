# kucoin_feed.py
# Multi-timeframe KuCoin data fetcher for Echo V Sniper Test Bot

import requests
import pandas as pd
import time
import os

KUCOIN_API_KEY = os.getenv("KUCOIN_API_KEY")
KUCOIN_URL = "https://api.kucoin.com/api/v1/market/candles"

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "KC-API-KEY": KUCOIN_API_KEY,
}

# Mapping for KuCoin intervals
INTERVAL_MAP = {
    "1m": "1min",
    "5m": "5min",
    "15m": "15min",
    "1h": "1hour"
}

# Fetch OHLCV data from KuCoin

def fetch_kucoin_ohlcv(symbol="BTC-USDT", interval="1m", limit=100):
    try:
        res = requests.get(KUCOIN_URL, params={
            "type": INTERVAL_MAP[interval],
            "symbol": symbol
        }, timeout=10)

        if res.status_code != 200:
            print(f"[KUCOIN ERROR] {res.status_code}: {res.text}")
            return None

        data = res.json().get("data", [])
        if not data:
            return None

        df = pd.DataFrame(data, columns=[
            "timestamp", "open", "close", "high", "low", "volume", "turnover"])

        df = df.iloc[::-1].reset_index(drop=True)
        df["timestamp"] = pd.to_datetime(df["timestamp"].astype(float), unit="ms")
        df[["open", "close", "high", "low", "volume"]] = df[["open", "close", "high", "low", "volume"]].astype(float)
        df["vwap"] = (df["high"] + df["low"] + df["close"]) / 3

        return df.head(limit)

    except Exception as e:
        print("[KUCOIN ERROR] API exception:", e)
        return None

# Collect multiple timeframe data

def get_multi_tf_kucoin_data():
    tf_data = {}
    for tf in ["1m", "5m", "15m", "1h"]:
        df = fetch_kucoin_ohlcv(interval=tf)
        if df is not None:
            tf_data[tf] = df
        else:
            print(f"[KUCOIN ERROR] No data for {tf}")
    return tf_data
