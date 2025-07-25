# kucoin_feed.py

import requests
import pandas as pd
import os
import time

KUCOIN_API_BASE = "https://api.kucoin.com"

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# KuCoin timeframes mapping
TIMEFRAME_MAP = {
    "1m": "1min",
    "5m": "5min",
    "15m": "15min",
    "1h": "1hour",
    "4h": "4hour"
}

def get_kucoin_ohlcv(symbol: str, timeframe: str, retries: int = 3):
    """
    Pulls clean KuCoin OHLCV data for a specific symbol and timeframe.
    """
    kucoin_tf = TIMEFRAME_MAP.get(timeframe)
    if not kucoin_tf:
        print(f"[KUCOIN ❌] Unsupported timeframe: {timeframe}")
        return None

    market = symbol.replace("/", "-").upper()  # BTC/USDT -> BTC-USDT
    endpoint = f"/api/v1/market/candles"
    params = {
        "type": kucoin_tf,
        "symbol": market,
        "startAt": int(time.time()) - 3600 * 48  # past 48h
    }

    for attempt in range(retries):
        try:
            url = f"{KUCOIN_API_BASE}{endpoint}"
            response = requests.get(url, headers=HEADERS, params=params, timeout=10)
            data = response.json()

            if "data" not in data or not data["data"]:
                print(f"[KUCOIN ⚠️] No data returned on attempt {attempt + 1}.")
                time.sleep(1)
                continue

            df = pd.DataFrame(data["data"], columns=[
                "timestamp", "open", "close", "high", "low", "volume", "turnover"
            ])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
            df = df.sort_values("timestamp")

            for col in ["open", "high", "low", "close", "volume"]:
                df[col] = pd.to_numeric(df[col], errors="coerce")

            return df[["timestamp", "open", "high", "low", "close", "volume"]]

        except Exception as e:
            print(f"[KUCOIN ERROR] Attempt {attempt + 1}: {e}")
            time.sleep(1)

    print("[KUCOIN ❌] All retries failed.")
    return None

def get_multi_tf_ohlcv(symbol="BTC-USDT", timeframes=None):
    """
    Returns a dictionary of DataFrames keyed by timeframe.
    """
    if timeframes is None:
        timeframes = ["1m", "5m", "15m", "1h", "4h"]

    tf_data = {}
    for tf in timeframes:
        df = get_kucoin_ohlcv(symbol, tf)
        if df is not None and not df.empty:
            tf_data[tf] = df
        else:
            print(f"[KUCOIN SKIP] {tf} returned no usable data.")
    return tf_data
