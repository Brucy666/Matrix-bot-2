# echo_v_engine.py
# AI-powered Echo V Engine with multi-timeframe aggregation + safe string handling

import pandas as pd
import numpy as np
from statistics import mean

# --- Heikin Ashi Simulation ---
def heikin_ashi(df):
    ha = pd.DataFrame(index=df.index)
    ha['close'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4
    ha['open'] = df['open']
    ha['high'] = df[['open', 'close', 'high']].max(axis=1)
    ha['low'] = df[['open', 'close', 'low']].min(axis=1)
    return ha

# --- Smoothed RSI ---
def compute_smoothed_rsi(prices, period=14, smooth=2):
    delta = prices.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.rolling(window=smooth).mean()

# --- Echo Pattern Logic ---
def detect_echo_vsplit(df):
    try:
        ha = heikin_ashi(df)
        fast = compute_smoothed_rsi(ha['close'], period=14, smooth=2)
        slow = compute_smoothed_rsi(ha['close'], period=14, smooth=8)

        fast_last = fast.iloc[-1]
        fast_prev = fast.iloc[-2]
        slow_last = slow.iloc[-1]
        slow_prev = slow.iloc[-2]

        # Echo pattern logic
        if fast_prev < slow_prev and fast_last > slow_last:
            return {"status": "Echo V-Split Bullish", "strength": 2.0, "reason": "Fast crossed above Slow"}
        elif fast_prev > slow_prev and fast_last < slow_last:
            return {"status": "Echo V-Split Bearish", "strength": 2.0, "reason": "Fast crossed below Slow"}
        elif abs(fast_last - slow_last) < 1.5 and abs(fast_prev - slow_prev) < 1.5:
            return {"status": "Echo Sync Flat", "strength": 1.0, "reason": "Fast/Slow tracking closely"}
        elif fast_last > slow_last and fast_prev > slow_prev:
            return {"status": "Echo Sync Up", "strength": 1.5, "reason": "Both rising"}
        elif fast_last < slow_last and fast_prev < slow_prev:
            return {"status": "Echo Sync Down", "strength": 1.5, "reason": "Both falling"}
        elif fast_last < 20 and fast_prev < 30 and slow_last < 30:
            return {"status": "Echo Collapse Bearish", "strength": 1.8, "reason": "Oversold collapse"}
        elif fast_last > 80 and fast_prev > 70 and slow_last > 70:
            return {"status": "Echo Collapse Bullish", "strength": 1.8, "reason": "Overbought surge"}

        return {"status": "None", "strength": 0.0, "reason": "No clear signal"}

    except Exception as e:
        return {"status": "Error", "strength": 0.0, "reason": str(e)}

# --- Multi-Timeframe Echo Aggregation ---
def get_multi_tf_echo_signals(tf_data_map: dict) -> dict:
    """
    Expects: { "1m": df, "3m": df, ... }
    Returns: { summary: [], bias: str, avg_strength: float }
    """
    summary = []
    types = []

    for tf, df in tf_data_map.items():
        if df is None or len(df) < 20:
            continue

        signal = detect_echo_vsplit(df)
        types.append(signal["status"])
        summary.append({
            "timeframe": tf,
            "signal": signal["status"],
            "strength": signal["strength"],
            "reason": signal["reason"]
        })

    if not summary:
        return {
            "summary": [],
            "bias": "No Data",
            "avg_strength": 0.0
        }

    valid = [s for s in summary if s["signal"] not in ["None", "Error"]]
    if not valid:
        return {
            "summary": summary,
            "bias": "Neutral",
            "avg_strength": round(mean([s["strength"] for s in summary]), 2)
        }

    # Count top bias
    top = max(set([v["signal"] for v in valid]), key=[v["signal"] for v in valid].count)
    avg_strength = round(mean([v["strength"] for v in valid if v["signal"] == top]), 2)

    return {
        "summary": summary,
        "bias": top,
        "avg_strength": avg_strength
    }
