# kucoin_feed.py
import requests
import pandas as pd
from datetime import datetime
import numpy as np

KUCOIN_API_KEY = "your_key_here"  # Replace if needed or pull from environment

# ---- Configurable Timeframes ----
TIMEFRAMES = ["1m", "5m", "15m", "1h", "4h"]

# ---- Fetch KuCoin OHLCV for a given timeframe ----
def fetch_ohlcv(symbol="BTC/USDT", interval="1m", limit=150):
    try:
        base = f"https://api.kucoin.com/api/v1/market/candles?type={interval}&symbol={symbol.replace('/', '-')}&limit={limit}"
        response = requests.get(base)
        raw = response.json()

        if "data" not in raw or not raw["data"]:
            print(f"[KUCOIN ERROR] No data returned for {interval}")
            return None

        # Convert to DataFrame
        df = pd.DataFrame(raw["data"], columns=[
            "timestamp", "open", "close", "high", "low", "volume", "turnover"
        ])

        df = df[::-1].copy()  # oldest to newest
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)
        return df

    except Exception as e:
        print(f"[KUCOIN ERROR] Failed to fetch {interval} OHLCV:", e)
        return None

# ---- RSI Calculation ----
def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# ---- Main Feed Generator for Multi-Timeframe ----
def get_multi_ohlcv(symbol="BTC/USDT"):
    try:
        tf_data_map = {}
        base_df = None

        for tf in TIMEFRAMES:
            df = fetch_ohlcv(symbol, interval=tf)
            if df is not None:
                df["rsi"] = calculate_rsi(df["close"])
                tf_data_map[tf] = df
                if tf == "1m":
                    base_df = df

        if base_df is None or len(base_df) < 10:
            print("[KUCOIN TEST ERROR] Base timeframe data (1m) invalid.")
            return None

        last_close = float(base_df["close"].iloc[-1])
        vwap = np.average(base_df["close"], weights=base_df["volume"])
        rsi_now = float(base_df["rsi"].iloc[-1])
        bias = "Above" if last_close > vwap else "Below"

        return {
            "price": last_close,
            "vwap": round(vwap, 2),
            "rsi": round(rsi_now, 2),
            "spoof": 0.0,  # placeholder, override later
            "bias": bias,
            "ohlcv": tf_data_map
        }

    except Exception as e:
        print("[KUCOIN TEST ERROR]", str(e))
        return None
