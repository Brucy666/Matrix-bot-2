# macro_vsplit_engine.py
# Detects macro V-Split RSI zones on KuCoin using 4H, 8H, and 1D data

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

KUCOIN_API = "https://api.kucoin.com"


def fetch_kucoin_ohlcv(symbol="BTC-USDT", interval="4hour", limit=100):
    try:
        url = f"{KUCOIN_API}/api/v1/market/candles"
        params = {"type": interval, "symbol": symbol.replace("/", "-"), "limit": limit}
        res = requests.get(url, params=params, timeout=10)
        data = res.json().get("data", [])
        df = pd.DataFrame(data, columns=["timestamp", "open", "close", "high", "low", "volume", "turnover"])
        df = df.astype(float)
        df = df.iloc[::-1]  # reverse chronological
        df["vwap"] = df["turnover"] / df["volume"]
        delta = df["close"].diff()
        gain = delta.clip(lower=0).rolling(window=14).mean()
        loss = -delta.clip(upper=0).rolling(window=14).mean()
        rs = gain / loss
        df["rsi"] = 100 - (100 / (1 + rs))
        return df
    except Exception as e:
        print(f"[MACRO VSPLIT] Feed error ({interval}):", e)
        return None


def detect_macro_vsplit(df):
    if df is None or len(df) < 20:
        return None

    try:
        recent_rsi = df["rsi"].iloc[-5:].values
        rsi_now = recent_rsi[-1]
        rsi_avg = np.mean(recent_rsi[:-1])
        
        vsplit_score = round(rsi_now - rsi_avg, 2)

        if vsplit_score > 8:
            return {"status": "Expansion Top", "score": vsplit_score}
        elif vsplit_score < -8:
            return {"status": "Expansion Bottom", "score": vsplit_score}
        elif abs(vsplit_score) > 3:
            return {"status": "Compression Zone", "score": vsplit_score}
        else:
            return {"status": "Flat", "score": vsplit_score}

    except Exception as e:
        print("[MACRO VSPLIT] Detection error:", e)
        return None


def get_macro_vsplit_summary():
    timeframes = ["4hour", "8hour", "1day"]
    summary = {}

    for tf in timeframes:
        df = fetch_kucoin_ohlcv(interval=tf)
        result = detect_macro_vsplit(df)
        if result:
            summary[tf] = result

    return summary


if __name__ == "__main__":
    print("[TEST] Macro VSplit Summary:")
    print(get_macro_vsplit_summary())
