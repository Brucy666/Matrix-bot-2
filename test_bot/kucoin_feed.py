# kucoin_feed.py

import requests
import pandas as pd
import os
import json

KUCOIN_API_BASE = "https://api.kucoin.com"

# Fallback mock file path
FALLBACK_DATA_DIR = "test_data"

# Hardcoded fallback timeframes for stability
TIMEFRAME_MAP = {
    "15m": "15min"
}

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def get_multi_tf_ohlcv(symbol: str, timeframe: str):
    """
    Attempt to fetch OHLCV data from KuCoin API, else load from fallback file.
    """
    try:
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
        response = requests.get(url, headers=HEADERS, params=params)
        data = response.json()

        if not data.get("data"):
            raise ValueError("Empty data")

        df = pd.DataFrame(data["data"], columns=[
            "timestamp", "open", "close", "high", "low", "volume", "turnover"
        ])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
        df = df.sort_values("timestamp")

        return df[["timestamp", "open", "high", "low", "close", "volume"]]

    except Exception as e:
        print(f"[KUCOIN ERROR] API failed for {symbol} {timeframe}: {e}")
        return load_fallback_ohlcv(symbol, timeframe)

def load_fallback_ohlcv(symbol: str, timeframe: str):
    """
    Load fallback OHLCV data from local JSON file.
    """
    try:
        filename = f"{symbol.replace('/', '-')}_{timeframe}.json"
        path = os.path.join(FALLBACK_DATA_DIR, filename)
        with open(path, "r") as f:
            raw = json.load(f)

        df = pd.DataFrame(raw)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp")

        print(f"[FALLBACK] Loaded {len(df)} candles for {symbol} {timeframe}")
        return df

    except Exception as e:
        print(f"[FALLBACK ERROR] Could not load fallback for {symbol} {timeframe}: {e}")
        return None
