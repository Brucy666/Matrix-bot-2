# kucoin_feed.py

import requests
import pandas as pd

KUCOIN_API_BASE = "https://api.kucoin.com"

# KuCoin timeframes accepted by the API
TIMEFRAME_MAP = {
    "1m": "1min",
    "5m": "5min",
    "15m": "15min",
    "1h": "1hour",
    "4h": "4hour"
}

def get_multi_tf_ohlcv(symbol: str, timeframes: list):
    """
    Fetch OHLCV data for multiple timeframes for a KuCoin symbol.
    Returns a dictionary of timeframe: DataFrame or None.
    """
    results = {}
    market = symbol.replace("/", "-").upper()  # BTC/USDT -> BTC-USDT

    for tf in timeframes:
        kucoin_tf = TIMEFRAME_MAP.get(tf)
        if not kucoin_tf:
            print(f"[KUCOIN ❌] Unsupported timeframe: {tf}")
            results[tf] = None
            continue

        try:
            endpoint = f"/api/v1/market/candles"
            params = {
                "type": kucoin_tf,
                "symbol": market,
                "startAt": int(pd.Timestamp.utcnow().timestamp()) - 3600 * 24 * 2,
            }
            url = f"{KUCOIN_API_BASE}{endpoint}"
            response = requests.get(url, params=params)
            data = response.json()

            if not data.get("data"):
                print(f"[KUCOIN SKIP] {tf} returned no usable data.")
                results[tf] = None
                continue

            df = pd.DataFrame(data["data"], columns=[
                "timestamp", "open", "close", "high", "low", "volume", "turnover"
            ])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
            df = df.sort_values("timestamp")
            results[tf] = df[["timestamp", "open", "high", "low", "close", "volume"]]

        except Exception as e:
            print(f"[KUCOIN ERROR] Failed to fetch {tf} for {symbol}: {e}")
            results[tf] = None

    return results
