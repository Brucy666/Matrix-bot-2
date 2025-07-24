# echo_v_engine.py
# AI-powered Echo V Engine using Heikin Ashi + multi-timeframe support

import pandas as pd
import numpy as np

# ----- Heikin Ashi Simulation -----
def heikin_ashi(df):
    ha = pd.DataFrame(index=df.index)
    ha['close'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4
    ha['open'] = df['open']
    ha['high'] = df[['open', 'close', 'high']].max(axis=1)
    ha['low'] = df[['open', 'close', 'low']].min(axis=1)
    return ha

# ----- Smoothed RSI Calculation -----
def compute_smoothed_rsi(prices, period=14, smooth=2):
    delta = prices.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.rolling(window=smooth).mean()

# ----- Echo V Pattern Detection -----
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
            return {"status": "Echo V-Split Bullish", "strength": 2.0}
        elif fast_prev > slow_prev and fast_last < slow_last:
            return {"status": "Echo V-Split Bearish", "strength": 2.0}
        elif abs(fast_last - slow_last) < 1.5 and abs(fast_prev - slow_prev) < 1.5:
            return {"status": "Echo Sync Flat", "strength": 1.0}
        elif fast_last > slow_last and fast_prev > slow_prev:
            return {"status": "Echo Sync Up", "strength": 1.5}
        elif fast_last < slow_last and fast_prev < slow_prev:
            return {"status": "Echo Sync Down", "strength": 1.5}
        elif fast_last < 20 and fast_prev < 30 and slow_last < 30:
            return {"status": "Echo Collapse Bearish", "strength": 1.8}
        elif fast_last > 80 and fast_prev > 70 and slow_last > 70:
            return {"status": "Echo Collapse Bullish", "strength": 1.8}

        return {"status": "None", "strength": 0.0}
    except Exception as e:
        print("[Echo Engine ERROR]", str(e))
        return {"status": "Error", "strength": 0.0}

# ----- Multi-Timeframe Echo Aggregator -----
def get_multi_tf_echo_signals(tf_data_map: dict) -> dict:
    """
    Aggregates Echo V signals across multiple timeframes.
    Expects: { "1m": df_1m, "3m": df_3m, "15m": df_15m, ... }
    Returns summary with dominant signal and avg strength.
    """
    from statistics import mean

    summary = []
    echo_types = []

    for tf, df in tf_data_map.items():
        if df is None or len(df) < 10:
            continue

        result = detect_echo_vsplit(df)
        echo_types.append(result["status"])
        summary.append({
            "tf": tf,
            "signal": result["status"],
            "strength": result["strength"]
        })

    if not summary:
        return {"summary": [], "bias": "Neutral", "avg_strength": 0.0}

    types = [s["signal"] for s in summary if s["signal"] not in ["None", "Error"]]
    grouped = {t: types.count(t) for t in set(types)}

    if not grouped:
        avg = mean([s["strength"] for s in summary])
        return {"summary": summary, "bias": "Neutral", "avg_strength": round(avg, 2)}

    top_type = max(grouped, key=grouped.get)
    confidence = mean([s["strength"] for s in summary if s["signal"] == top_type])

    return {
        "summary": summary,
        "bias": top_type,
        "avg_strength": round(confidence, 2)
    }
