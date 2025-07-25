# kucoin_feed.py

import requests
import pandas as pd

KUCOIN_API_BASE = "https://api.kucoin.com"

# Map our internal timeframes to KuCoin's naming
TIMEFRAME_MAP = {
    "1m": "1min",
    "5m": "5min",
    "15m": "15min",
    "1h": "1hour",
    "4h": "4hour"
}

def get_ohlcv(symbol: str, timeframe: str):
    """Fetch OHLCV data for one timeframe."""
    try:
        tf = TIMEFRAME_MAP.get(timeframe)
        if not tf:
            print(f"[KUCOIN ❌] Unsupported timeframe: {timeframe}")
            return None

        market = symbol.replace("/", "-").upper()
        endpoint = f"/api/v1/market/candles"
        params = {
            "type": tf,
            "symbol": market,
            "startAt": int(pd.Timestamp.utcnow().timestamp()) - 60 * 60 * 24 * 2
        }

        url = KUCOIN_API_BASE + endpoint
        response = requests.get(url, params=params)
        data = response.json()

        if not data.get("data"):
            print(f"[KUCOIN ERROR] No data returned for {timeframe}. Response: {data}")
            return None

        df = pd.DataFrame(data["data"], columns=[
            "timestamp", "open", "close", "high", "low", "volume", "turnover"
        ])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
        df = df.sort_values("timestamp")
        return df[["timestamp", "open", "high", "low", "close", "volume"]]

    except Exception as e:
        print(f"[KUCOIN ERROR] Failed for {timeframe}: {e}")
        return None

def get_multi_tf_ohlcv(symbol: str, timeframes: list):
    """Pull multiple timeframes and return them as a dictionary of DataFrames."""
    tf_data = {}
    for tf in timeframes:
        df = get_ohlcv(symbol, tf)
        if df is not None:
            tf_data[tf] = df
        else:
            print(f"[KUCOIN SKIP] {tf} returned no usable data.")
    return tf_data
