# macro_vsplit_engine.py
# Multi-Timeframe RSI-V Macro Split Engine (KuCoin Live Data)

import pandas as pd
from datetime import datetime
from kucoin_feed import get_kucoin_sniper_feed

# Timeframe config and bias type
TIMEFRAMES = {
    "1D": {"interval": "1day", "bias": "macro"},
    "8H": {"interval": "8hour", "bias": "trend"},
    "4H": {"interval": "4hour", "bias": "momentum"},
    "1H": {"interval": "1hour", "bias": "setup"},
    "30M": {"interval": "30min", "bias": "entry"},
}

# V-Split detection on RSI/Price divergence
def detect_rsi_vsplit(df):
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

# Run scan on multiple timeframes
def run_macro_vsplit_scan():
    print("\n[MACRO 🧠] Starting RSI-V Macro Split Scan...\n")
    active_splits = []

    for tf, cfg in TIMEFRAMES.items():
        print(f"[CHECK] {tf} RSI-V data...")
        df = get_kucoin_sniper_feed(symbol="BTC-USDT", interval=cfg["interval"])
        result = detect_rsi_vsplit(df)

        if result:
            active_splits.append({
                "timeframe": tf,
                "bias": cfg["bias"],
                "type": result,
                "rsi": round(df['rsi'].iloc[-1], 2),
                "price": round(df['close'].iloc[-1], 2)
            })

    if not active_splits:
        print("[MACRO 🧠] No V-Split signals detected.\n")
    else:
        print("\n[MACRO ✅] Active RSI-V Splits Detected:")
        for e in active_splits:
            print(f"→ {e['timeframe']} ({e['bias']}): {e['type']} | RSI: {e['rsi']} | Price: {e['price']}")

    return active_splits

# Script entry
if __name__ == "__main__":
    run_macro_vsplit_scan()
