# vsplit_curve_engine.py
# Advanced RSI-V Curve Split Analyzer for Multi-Timeframe Momentum Scanning

import numpy as np
from kucoin_feed import get_kucoin_sniper_feed

# Timeframes to scan and their labels
VSPLIT_TIMEFRAMES = {
    "1D": "macro",
    "8H": "trend",
    "4H": "momentum",
    "2H": "setup",
    "1H": "trigger",
    "30m": "micro",
    "12m": "entry",
    "3m": "scalp"
}

def detect_vsplit_sling(df, tf=""):
    try:
        if df is None or len(df) < 20 or "fast" not in df or "slow" not in df:
            return None

        fast = df["fast"].astype(float).tolist()
        slow = df["slow"].astype(float).tolist()
        close = df["close"].astype(float).tolist()

        # Recent slopes
        fast_slope = fast[-1] - fast[-5]
        slow_slope = slow[-1] - slow[-5]

        # Compression: how tight they were before the split
        compression = abs(np.mean(fast[-10:]) - np.mean(slow[-10:]))
        split_now = abs(fast[-1] - slow[-1])

        split_delta = split_now - compression
        compression_ratio = split_now / compression if compression > 0 else 0

        # Direction and energy scoring
        if fast_slope > 0 and slow_slope > 0 and fast[-1] > slow[-1]:
            direction = "Bullish"
        elif fast_slope < 0 and slow_slope < 0 and fast[-1] < slow[-1]:
            direction = "Bearish"
        else:
            direction = "Neutral"

        # Energy scoring logic
        energy = (
            abs(fast_slope) +
            abs(slow_slope) +
            split_delta +
            compression_ratio
        )

        confidence = round(min(max(energy / 10, 0), 10), 1)

        return {
            "timeframe": tf,
            "bias": direction,
            "phase": "Slingshot" if direction != "Neutral" else "None",
            "fast_slope": round(fast_slope, 2),
            "slow_slope": round(slow_slope, 2),
            "compression_ratio": round(compression_ratio, 2),
            "split_size": round(split_now, 2),
            "confidence": confidence
        }

    except Exception as e:
        print(f"[!] V-Split error: {e}")
        return None

def scan_vsplit_across_timeframes(symbol="BTCUSDT"):
    results = []
    print("\n[🧠] Starting RSI-V Curve Scan...\n")

    for tf, label in VSPLIT_TIMEFRAMES.items():
        df = get_kucoin_sniper_feed(symbol=symbol, interval=tf)
        result = detect_vsplit_sling(df, tf=tf)
        if result:
            print(f"→ {tf}: {result['bias']} | Score: {result['confidence']} | Slope Δ: {result['fast_slope']} / {result['slow_slope']}")
            results.append(result)

    if not results:
        print("[🧠] No strong V-Split signals detected.")
    return results

if __name__ == "__main__":
    scan_vsplit_across_timeframes()
