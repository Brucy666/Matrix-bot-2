# kucoin_feed.py (Updated Fallback Version)

import requests
import pandas as pd
import os

KUCOIN_API_BASE = "https://api.kucoin.com"

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Most reliable KuCoin timeframes
TIMEFRAME_PRIORITY = ["1day", "4hour", "1hour"]

CANDLE_COLUMNS = ["timestamp", "open", "close", "high", "low", "volume", "turnover"]


def fetch_ohlcv(symbol: str, kucoin_tf: str):
    """Fetch OHLCV data from KuCoin for a given symbol and timeframe."""
    try:
        market = symbol.replace("/", "-").upper()
        endpoint = f"/api/v1/market/candles"
        params = {
            "type": kucoin_tf,
            "symbol": market,
            "startAt": int(pd.Timestamp.utcnow().timestamp()) - 3600 * 24 * 5,
        }
        url = f"{KUCOIN_API_BASE}{endpoint}"
        response = requests.get(url, headers=HEADERS, params=params)
        data = response.json()

        if not data.get("data"):
            print(f"[KUCOIN ERROR] No data for {kucoin_tf}. Response: {data}")
            return None

        df = pd.DataFrame(data["data"], columns=CANDLE_COLUMNS)
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
        df = df.sort_values("timestamp")
        return df[["timestamp", "open", "high", "low", "close", "volume"]]

    except Exception as e:
        print(f"[KUCOIN EXCEPTION] Failed fetch {kucoin_tf}: {e}")
        return None


def get_best_ohlcv(symbol: str):
    """Try multiple fallback timeframes and return the first valid DataFrame."""
    for tf in TIMEFRAME_PRIORITY:
        print(f"[KUCOIN ⏳] Trying timeframe: {tf}")
        df = fetch_ohlcv(symbol, tf)
        if df is not None and not df.empty:
            print(f"[KUCOIN ✅] Using {tf} timeframe with {len(df)} candles.")
            return df
        print(f"[KUCOIN ❌] Skipped {tf} — unusable.")

    print(f"[KUCOIN TEST ERROR] No valid timeframe found. Aborting Echo V.")
    return None
