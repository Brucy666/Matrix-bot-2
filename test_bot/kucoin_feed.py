# kucoin_feed.py

import requests
import pandas as pd
import os

KUCOIN_API_BASE = "https://api.kucoin.com"

# Standard headers if needed
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Supported KuCoin timeframes
TIMEFRAME_MAP = {
    "1m": "1min",
    "5m": "5min",
    "15m": "15min",
    "1h": "1hour",
    "4h": "4hour"
}

def get_multi_tf_ohlcv(symbol: str, timeframe: str):
    """
    Fetch OHLCV data for a given symbol and timeframe from KuCoin.
    Returns a pandas DataFrame or None if the data is not available.
    """
    try:
        kucoin_tf = TIMEFRAME_MAP.get(timeframe)
        if not kucoin_tf:
            print(f"[KUCOIN ❌] Unsupported timeframe: {timeframe}")
            return None

        market = symbol.replace("/", "-").upper()  # e.g., BTC/USDT -> BTC-USDT
        endpoint = f"/api/v1/market/candles"
        params = {
            "type": kucoin_tf,
            "symbol": market,
            "startAt": int(pd.Timestamp.utcnow().timestamp()) - 3600 * 24 * 2,  # last 2 days
        }

        url = f"{KUCOIN_API_BASE}{endpoint}"
        response = requests.get(url, headers=HEADERS, params=params)
        data = response.json()

        if not data.get("data"):
            print(f"[KUCOIN SKIP] {timeframe} returned no usable data.")
            return None

        # Convert data to DataFrame
        df = pd.DataFrame(data["data"], columns=[
            "timestamp", "open", "close", "high", "low", "volume", "turnover"
        ])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
        df = df.sort_values("timestamp")

        return df[["timestamp", "open", "high", "low", "close", "volume"]]

    except Exception as e:
        print(f"[KUCOIN ERROR] Failed to fetch OHLCV for {symbol} {timeframe}: {e}")
        return None
