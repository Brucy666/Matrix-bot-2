# kucoin_feed.py

import requests
import pandas as pd
import os
import json

KUCOIN_API_BASE = "https://api.kucoin.com"

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

TIMEFRAME_MAP = {
    "1m": "1min",
    "5m": "5min",
    "15m": "15min",
    "1h": "1hour",
    "4h": "4hour"
}

FALLBACK_DATA_DIR = "test_data"


def get_multi_tf_ohlcv(symbol: str, timeframe: str):
    kucoin_tf = TIMEFRAME_MAP.get(timeframe)
    if not kucoin_tf:
        print(f"[KUCOIN ERROR] Unsupported timeframe: {timeframe}")
        return None

    market = symbol.replace("/", "-").upper()
    endpoint = "/api/v1/market/candles"
    params = {
        "type": kucoin_tf,
        "symbol": market,
        "startAt": int(pd.Timestamp.utcnow().timestamp()) - 3600 * 24 * 2,
    }

    url = f"{KUCOIN_API_BASE}{endpoint}"

    try:
        response = requests.get(url, headers=HEADERS, params=params)
        data = response.json()

        if not data.get("data"):
            raise ValueError("Empty response")

        df = pd.DataFrame(data["data"], columns=[
            "timestamp", "open", "close", "high", "low", "volume", "turnover"
        ])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
        df = df.sort_values("timestamp")
        return df[["timestamp", "open", "high", "low", "close", "volume"]]

    except Exception as e:
        print(f"[KUCOIN ERROR] Live API failed: {e}. Trying fallback file...")
        return load_fallback_ohlcv(symbol, timeframe)


def load_fallback_ohlcv(symbol: str, timeframe: str):
    filename = f"{symbol.replace('/', '-')}_{timeframe}.json"
    filepath = os.path.join(FALLBACK_DATA_DIR, filename)
    try:
        with open(filepath, "r") as f:
            raw = json.load(f)
        df = pd.DataFrame(raw[1:], columns=raw[0])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
        df = df.sort_values("timestamp")
        print(f"[KUCOIN FALLBACK] Loaded local OHLCV: {filename}")
        return df[["timestamp", "open", "high", "low", "close", "volume"]]
    except Exception as e:
        print(f"[KUCOIN FALLBACK ERROR] Could not load fallback {filename}: {e}")
        return None
