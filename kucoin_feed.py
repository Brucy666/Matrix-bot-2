# kucoin_feed.py
# Fetch KuCoin candlestick data and calculate RSI + VWAP for any timeframe

import requests
import pandas as pd
import numpy as np

KUCOIN_URL = "https://api.kucoin.com"

# Main fetch function
def get_kucoin_sniper_feed(symbol="BTC-USDT", interval="1min", limit=100):
    try:
        url = f"{KUCOIN_URL}/api/v1/market/candles"
        params = {
            "symbol": symbol,
            "type": interval,
            "limit": limit
        }
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        raw = response.json().get("data", [])

        if not raw or len(raw) < 20:
            return None

        raw.reverse()  # Ensure ascending order

        df = pd.DataFrame(raw, columns=[
            "timestamp", "open", "close", "high", "low", "volume", "turnover"
        ])

        df = df.astype(float)
        df["vwap"] = df["turnover"] / df["volume"]

        delta = df["close"].diff()
        gain = delta.clip(lower=0).rolling(window=14).mean()
        loss = -delta.clip(upper=0).rolling(window=14).mean()
        rs = gain / loss
        df["rsi"] = 100 - (100 / (1 + rs))
        df["rsi"] = df["rsi"].fillna(50)

        return df.tail(20)

    except Exception as e:
        print(f"[!] KuCoin Feed Error: {e}")
        return None

# Dummy for future L2 spoof scoring if needed
def fetch_orderbook():
    return {"bids": 1.0, "asks": 1.0}
