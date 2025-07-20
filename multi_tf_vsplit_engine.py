# multi_tf_vsplit_engine.py
# Detects RSI V-type patterns across multiple timeframes for macro bias scoring

from rsi_vsplit_engine import detect_rsi_vsplit
from kucoin_feed import get_kucoin_sniper_feed

TIMEFRAMES = {
    "1D": "1d",
    "8H": "8h",
    "4H": "4h",
    "1H": "1h",
    "30M": "30m"
}

def scan_multi_tf_rsi(symbol="BTCUSDT") -> tuple:
    results = []
    bias_counts = {"Bull": 0, "Bear": 0}

    for label, interval in TIMEFRAMES.items():
        df = get_kucoin_sniper_feed(symbol=symbol, interval=interval)
        if df is None or len(df) < 20:
            continue

        fast = df["rsi"].astype(float).tolist()
        slow = df["rsi"].rolling(8).mean().fillna(50).astype(float).tolist()
        signal = detect_rsi_vsplit(fast, slow)

        if not signal["type"]:
            continue

        results.append({
            "timeframe": label,
            "type": signal["type"],
            "strength": signal["strength"],
            "reason": signal["reason"]
        })

        # Count bias direction
        if signal["type"] in ["RSI V-Split", "RSI Sync Up"]:
            bias_counts["Bull"] += 1
        elif signal["type"] in ["RSI Collapse", "RSI Sync Down"]:
            bias_counts["Bear"] += 1

    # Final macro bias decision
    if bias_counts["Bull"] >= 3:
        macro_bias = "Strong Bull"
    elif bias_counts["Bear"] >= 3:
        macro_bias = "Strong Bear"
    elif bias_counts["Bull"] == bias_counts["Bear"] and bias_counts["Bull"] > 0:
        macro_bias = "Mixed"
    elif bias_counts["Bull"] + bias_counts["Bear"] == 0:
        macro_bias = "No Bias"
    else:
        macro_bias = "Mixed"

    return results, macro_bias
