# kucoin_feed.py
# Stable KuCoin feed fetcher for sniper engine (fixed)

import pandas as pd
import requests

KUCOIN_SYMBOL = "BTC-USDT"
KUCOIN_ENDPOINT = f"https://api.kucoin.com/api/v1/market/candles"

def get_kucoin_sniper_feed():
    try:
        params = {
            "type": "1min",
            "symbol": KUCOIN_SYMBOL
        }
        res = requests.get(KUCOIN_ENDPOINT, params=params)
        if res.status_code != 200:
            print("[KuCoin ERROR] HTTP", res.status_code)
            return None

        data = res.json()
        if "data" not in data or not isinstance(data["data"], list):
            print("[KuCoin ERROR] Invalid data format:", data)
            return None

        candles = data["data"]
        df = pd.DataFrame(candles, columns=[
            "timestamp", "open", "close", "high", "low", "volume", "turnover"
        ])
        df = df.iloc[::-1].copy()
        df[["open", "close", "high", "low", "volume"]] = df[["open", "close", "high", "low", "volume"]].astype(float)
        df["timestamp"] = pd.to_datetime(df["timestamp"].astype("int64"), unit="ms")

        # Calculate RSI
        df["delta"] = df["close"].diff()
        df["gain"] = df["delta"].clip(lower=0)
        df["loss"] = -df["delta"].clip(upper=0)
        df["avg_gain"] = df["gain"].rolling(14).mean()
        df["avg_loss"] = df["loss"].rolling(14).mean()
        rs = df["avg_gain"] / df["avg_loss"]
        df["rsi"] = 100 - (100 / (1 + rs))

        # VWAP estimate
        df["vwap"] = (df["close"] * df["volume"]).cumsum() / df["volume"].cumsum()

        return df.dropna()

    except Exception as e:
        print("[KuCoin FEED ERROR]", e)
        return None


def fetch_orderbook():
    try:
        url = f"https://api.kucoin.com/api/v1/market/orderbook/level2_100"
        params = {"symbol": KUCOIN_SYMBOL}
        res = requests.get(url, params=params).json()
        bids = sum(float(x[1]) for x in res["data"]["bids"])
        asks = sum(float(x[1]) for x in res["data"]["asks"])
        return {"bids": bids, "asks": asks}
    except Exception as e:
        print("[KuCoin Orderbook ERROR]", e)
        return {"bids": 0, "asks": 0}
