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

def get_multi_tf_ohlcv(symbol: str, tf_key: str):
    """
    Fetches OHLCV data for a specific symbol and mapped KuCoin timeframe key (e.g., '1m', '5m').
    Returns DataFrame or None.
    """
    try:
        if tf_key not in TIMEFRAME_MAP:
            print(f"[KUCOIN ERROR] Unsupported timeframe: {tf_key}")
            return None

        tf_code = TIMEFRAME_MAP[tf_key]
        market = symbol.replace("/", "-").upper()  # e.g., BTC/USDT -> BTC-USDT

        end_time = int(datetime.utcnow().timestamp())
        start_time = end_time - 60 * 60 * 48  # last 48 hours

        params = {
            "symbol": market,
            "type": tf_code,
            "startAt": start_time,
            "endAt": end_time
        }

        url = f"{KUCOIN_API_BASE}/api/v1/market/candles"
        response = requests.get(url, headers=HEADERS, params=params)
        data = response.json()

        if data.get("code") != "200000" or not data.get("data"):
            print(f"[KUCOIN ERROR] No data returned for {symbol} {tf_key}. Full response: {data}")
            return None

        df = pd.DataFrame(data["data"], columns=[
            "timestamp", "open", "close", "high", "low", "volume", "turnover"
        ])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
        df = df.sort_values("timestamp")

        return df[["timestamp", "open", "high", "low", "close", "volume"]]

    except Exception as e:
        print(f"[KUCOIN ERROR] Exception during fetch for {symbol} {tf_key}: {str(e)}")
        return None
