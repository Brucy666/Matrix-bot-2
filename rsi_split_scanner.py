# rsi_split_scanner.py
# Scans and stores RSI-V Split signals across multiple timeframes

import requests
import pandas as pd
import numpy as np
from datetime import datetime
from memory_store import save_split_signal

TIMEFRAMES = {
    '1d': '1d',
    '12h': '12h',
    '4h': '4h',
    '1h': '1h',
    '30m': '30m',
    '15m': '15m',
    '6m': '5m',   # using 5m data
    '3m': '3m',
    '1m': '1m'
}

KUCOIN_KLINE_URL = "https://api.kucoin.com/api/v1/market/candles"


def fetch_ohlcv(symbol="BTC-USDT", interval="1m", limit=100):
    try:
        res = requests.get(KUCOIN_KLINE_URL, params={
            "symbol": symbol,
            "type": interval,
            "limit": limit
        }, timeout=5)
        candles = res.json().get("data", [])
        if not candles:
            return None
        df = pd.DataFrame(candles, columns=[
            "timestamp", "open", "close", "high", "low", "volume", "turnover"
        ])
        df = df.iloc[::-1].astype(float)
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        return df
    except Exception as e:
        print(f"[!] Fetch OHLCV error: {e}")
        return None


def compute_rsi(close_prices, period=14):
    delta = close_prices.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / (loss + 1e-9)
    return 100 - (100 / (1 + rs))


def detect_vsplit(rsi_series):
    if len(rsi_series) < 5:
        return False
    # Check for V shape
    return (
        rsi_series.iloc[-3] > rsi_series.iloc[-4] and
        rsi_series.iloc[-2] < rsi_series.iloc[-3] and
        rsi_series.iloc[-1] > rsi_series.iloc[-2]
    )


def scan_all_timeframes(symbol="BTC-USDT"):
    for label, interval in TIMEFRAMES.items():
        df = fetch_ohlcv(symbol, interval)
        if df is None or len(df) < 20:
            print(f"[✖] {label} — Insufficient data")
            continue

        df["rsi"] = compute_rsi(df["close"])
        if detect_vsplit(df["rsi"]):
            split = {
                "symbol": symbol,
                "timestamp": datetime.utcnow().isoformat(),
                "timeframe": label,
                "rsi_tail": [round(x, 2) for x in df["rsi"].tail(5).tolist()],
                "rsi_status": "V-Split"
            }
            save_split_signal(split)
            print(f"[✓] {label} RSI-V Split detected | {split['rsi_tail']}")
        else:
            print(f"[—] {label} No split")


if __name__ == "__main__":
    scan_all_timeframes()
