# kucoin_feed.py

import requests
import pandas as pd
from datetime import datetime, timedelta

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

def get_multi_tf_ohlcv(symbol: str, timeframe: str):
    """
    Fetch OHLCV data for a given trading pair and timeframe from KuCoin.
    Returns a pandas DataFrame with [timestamp, open, high, low, close, volume].
    """
    try:
        tf_code = TIMEFRAME_MAP.get(timeframe)
        if not tf_code:
            print(f"[KUCOIN ERROR] Unsupported timeframe: {timeframe}")
            return None

        market = symbol.replace("/", "-").upper()  # e.g., BTC/USDT -> BTC-USDT

        end_time = int(datetime.utcnow().timestamp())
        start_time = end_time - 2 * 24 * 60 * 60  # last 2 days in seconds

        url = f"{KUCOIN_API_BASE}/api/v1/market/candles"
        params = {
            "symbol": market,
            "type": tf_code,
            "startAt": start_time,
            "endAt": end_time
        }

        response = requests.get(url, headers=HEADERS, params=params)
        data = response.json()

        if data.get("code") != "200000" or "data" not in data or not data["data"]:
            print(f"[KUCOIN ERROR] No data returned for {symbol} {timeframe}. Full response: {data}")
            return None

        df = pd.DataFrame(data["data"], columns=[
            "timestamp", "open", "close", "high", "low", "volume", "turnover"
        ])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
        df = df.sort_values("timestamp")

        return df[["timestamp", "open", "high", "low", "close", "volume"]]

    except Exception as e:
        print(f"[KUCOIN ERROR] Exception during fetch for {symbol} {timeframe}: {str(e)}")
        return None
