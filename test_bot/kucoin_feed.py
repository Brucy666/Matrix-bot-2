# kucoin_feed.py
# Unified KuCoin data fetcher for Echo V AI & RSI-V engines

import requests
import pandas as pd
import os

API_KEY = os.getenv("KUCOIN_API_KEY")
BASE_URL = "https://api.kucoin.com/api/v1"

HEADERS = {
    "Accept": "application/json",
    "KC-API-KEY": API_KEY,
}

def get_kucoin_sniper_feed(symbol="BTC-USDT", interval="1m", limit=150):
    url = f"{BASE_URL}/market/candles?type={interval}&symbol={symbol}&limit={limit}"
    try:
        res = requests.get(url, headers=HEADERS)
        data = res.json()["data"]

        df = pd.DataFrame(data, columns=[
            "timestamp", "open", "close", "high", "low", "volume", "turnover"
        ])
        df = df.iloc[::-1].copy()
        df["timestamp"] = pd.to_datetime(pd.to_numeric(df["timestamp"]), unit="ms")
        df[["open", "close", "high", "low", "volume"]] = df[["open", "close", "high", "low", "volume"]].astype(float)
        df["vwap"] = (df["high"] + df["low"] + df["close"]) / 3
        return df

    except Exception as e:
        print("[KUCOIN ERROR]", e)
        return None

def get_multi_ohlcv(symbol="BTC-USDT", intervals=["1m", "5m", "15m", "1h", "4h"], limit=150):
    tf_data = {}
    for tf in intervals:
        df = get_kucoin_sniper_feed(symbol=symbol, interval=tf, limit=limit)
        if df is not None and not df.empty:
            tf_data[tf] = df
    return tf_data

def fetch_orderbook(symbol="BTC-USDT"):
    try:
        url = f"{BASE_URL}/market/orderbook/level2_20?symbol={symbol}"
        res = requests.get(url, headers=HEADERS)
        data = res.json()["data"]
        bids = sum(float(b[1]) for b in data["bids"])
        asks = sum(float(a[1]) for a in data["asks"])
        return {"bids": bids, "asks": asks}
    except Exception as e:
        print("[ORDERBOOK ERROR]", e)
        return {"bids": 1.0, "asks": 1.0}
