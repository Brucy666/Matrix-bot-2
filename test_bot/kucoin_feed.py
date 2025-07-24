# kucoin_feed.py
# Data feed module for test bot (Echo V + other tools)

import pandas as pd
import requests
import os
import numpy as np

KUCOIN_SYMBOL = "BTC-USDT"
API_BASE = "https://api.kucoin.com"

def fetch_klines(symbol=KUCOIN_SYMBOL, interval='1min', limit=100):
    try:
        url = f"{API_BASE}/api/v1/market/candles?type={interval}&symbol={symbol}&limit={limit}"
        res = requests.get(url)
        res.raise_for_status()
        data = res.json().get("data", [])

        if not data:
            print("[KuCoin FEED] No Kline data returned.")
            return None

        df = pd.DataFrame(data, columns=["timestamp", "open", "close", "high", "low", "volume", "_"])
        df = df.iloc[::-1]  # Reverse to chronological order

        # Convert to floats and timestamp
        for col in ["open", "high", "low", "close", "volume"]:
            df[col] = df[col].astype(float)
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

        # Calculate RSI
        delta = df["close"].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain / avg_loss
        df["rsi"] = 100 - (100 / (1 + rs))

        # Calculate simple VWAP for context
        df["vwap"] = (df["high"] + df["low"] + df["close"]) / 3

        return df.dropna().reset_index(drop=True)

    except Exception as e:
        print(f"[KuCoin FEED ERROR] {e}")
        return None

def get_kucoin_sniper_feed():
    return fetch_klines()

def fetch_orderbook(symbol=KUCOIN_SYMBOL):
    try:
        url = f"{API_BASE}/api/v1/market/orderbook/level2_100?symbol={symbol}"
        res = requests.get(url)
        res.raise_for_status()
        data = res.json().get("data", {})

        bids = sum(float(entry[1]) for entry in data.get("bids", []))
        asks = sum(float(entry[1]) for entry in data.get("asks", []))

        return {"bids": bids, "asks": asks}

    except Exception as e:
        print(f"[KuCoin Orderbook ERROR] {e}")
        return {"bids": 1, "asks": 1}
