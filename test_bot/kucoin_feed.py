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
    kucoin_tf = TIMEFRAME_MAP.get(timeframe)
    if not kucoin_tf:
        print(f"[KUCOIN ❌] Unsupported timeframe: {timeframe}")
        return None

    try:
        market = symbol.replace("/", "-").upper()
        endpoint = "/api/v1/market/candles"
        params = {
            "type": kucoin_tf,
            "symbol": market,
            "startAt": int(pd.Timestamp.utcnow().timestamp()) - 3600 * 24
        }

        url = f"{KUCOIN_API_BASE}{endpoint}"
        response = requests.get(url, headers=HEADERS, params=params)
        data = response.json()

        if not data.get("data"):
            print(f"[KUCOIN SKIP] {timeframe} returned no usable data.")
            return None

        df = pd.DataFrame(data["data"], columns=[
            "timestamp", "open", "close", "high", "low", "volume", "turnover"
        ])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
        df = df.sort_values("timestamp")
        return df[["timestamp", "open", "high", "low", "close", "volume"]]

    except Exception as e:
        print(f"[KUCOIN ERROR] {timeframe} fetch failed: {e}")
        return None
