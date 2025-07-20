# macro_vsplit_engine.py
# Multi-Timeframe RSI-V Macro Split Engine

import pandas as pd
from datetime import datetime
from kucoin_feed import get_kucoin_sniper_feed

# Timeframe config and color bias
TIMEFRAMES = {
    "1D": {"interval": "1d", "bias": "macro"},
    "8H": {"interval": "8h", "bias": "trend"},
    "4H": {"interval": "4h", "bias": "momentum"},
    "1H": {"interval": "1h", "bias": "setup"},
    "30M": {"interval": "30m", "bias": "entry"},
}

# Utility to fetch and calculate RSI-V per timeframe
def detect_rsi_vsplit(df, label=""):
    try:
        if df is None or len(df) < 20:
            return None
        rsi = df['rsi'].astype(float).tolist()
        price = df['close'].astype(float).tolist()

        if rsi[-1] > rsi[-2] and price[-1] < price[-2]:
            return "RSI V-Split (Bullish)"
        elif rsi[-1] < rsi[-2] and price[-1] > price[-2]:
            return "RSI V-Split (Bearish)"
        return None
    except:
        return None

# Run full macro sweep
def run_macro_vsplit_scan():
    print("\n[MACRO 🧠] Starting RSI-V Macro Split Scan...\n")

    active_splits = []

    for tf, config in TIMEFRAMES.items():
        interval = config["interval"]
        bias_type = config["bias"]

        print(f"[CHECK] Fetching {tf} RSI-V data...")

        df = get_kucoin_sniper_feed(symbol="BTCUSDT", interval=interval)
        vsplit_result = detect_rsi_vsplit(df)

        if vsplit_result:
            active_splits.append({
                "timeframe": tf,
                "bias": bias_type,
                "type": vsplit_result,
                "rsi": round(df['rsi'].iloc[-1], 2),
                "price": round(df['close'].iloc[-1], 2)
            })

    if not active_splits:
        print("[MACRO 🧠] No V-Split signals detected on any major timeframe.\n")
    else:
        print("\n[MACRO ✅] Active RSI-V Splits Detected:")
        for entry in active_splits:
            print(f"→ {entry['timeframe']} ({entry['bias']}): {entry['type']} | RSI: {entry['rsi']} | Price: {entry['price']}")

    return active_splits

# Entry point for testing manually
if __name__ == "__main__":
    run_macro_vsplit_scan()
