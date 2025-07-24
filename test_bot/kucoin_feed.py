# kucoin_feed.py
import os
import pandas as pd
import requests
from datetime import datetime
import numpy as np

KUCOIN_SYMBOL = "BTC-USDT"
BASE_URL = "https://api.kucoin.com"
KUCOIN_API_KEY = os.getenv("KUCOIN_API_KEY")

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def fetch_ohlcv(symbol: str, interval: str, limit: int = 300):
    url = f"{BASE_URL}/api/v1/market/candles?type={interval}&symbol={symbol}&limit={limit}"
    headers = {"KC-API-KEY": KUCOIN_API_KEY} if KUCOIN_API_KEY else {}
    try:
        res = requests.get(url, headers=headers)
        data = res.json().get("data", [])
        if not data:
            print("[KUCOIN API] Empty data for", interval)
            return None
        df = pd.DataFrame(data, columns=["timestamp", "open", "close", "high", "low", "volume", "turnover"])
        df["timestamp"] = pd.to_datetime(df["timestamp"].astype(float), unit="ms")
        df = df.sort_values("timestamp")
        df["close"] = df["close"].astype(float)
        df["rsi"] = compute_rsi(df["close"])
        return df
    except Exception as e:
        print("[KUCOIN ERROR]", e)
        return None

def get_multi_tf_kucoin_data():
    tf_map = {
        "1m": "1min",
        "3m": "3min",
        "15m": "15min"
    }

    tf_data_map = {}
    for tf, interval in tf_map.items():
        df = fetch_ohlcv(KUCOIN_SYMBOL, interval)
        if df is not None and "rsi" in df.columns:
            tf_data_map[tf] = df
        else:
            print(f"[KUCOIN FEED] Skipped {tf} — RSI or Data missing")

    return tf_data_map
