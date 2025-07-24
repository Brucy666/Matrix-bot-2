# echo_v_engine_v2.py
# Multi-Timeframe AI-Powered Echo V Engine for KuCoin Sniper System

import pandas as pd
import numpy as np

# --- Heikin Ashi Simulation ---
def heikin_ashi(df):
    ha = pd.DataFrame(index=df.index)
    ha['close'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4
    ha['open'] = df['open'].copy()
    ha['high'] = df[['open', 'close', 'high']].max(axis=1)
    ha['low'] = df[['open', 'close', 'low']].min(axis=1)
    return ha

# --- Smoothed RSI Calculation ---
def compute_smoothed_rsi(prices, period=14, smooth=2):
    delta = prices.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.rolling(window=smooth).mean()

# --- Echo V Split Pattern Detection ---
def detect_echo_vsplit(df):
    try:
        ha = heikin_ashi(df)
        fast = compute_smoothed_rsi(ha['close'], period=14, smooth=2)
        slow = compute_smoothed_rsi(ha['close'], period=14, smooth=8)

        fast_last, fast_prev = fast.iloc[-1], fast.iloc[-2]
        slow_last, slow_prev = slow.iloc[-1], slow.iloc[-2]

        if fast_prev < slow_prev and fast_last > slow_last:
            return ("Echo V-Split Bullish", 2.0)
        elif fast_prev > slow_prev and fast_last < slow_last:
            return ("Echo V-Split Bearish", 2.0)
        elif abs(fast_last - slow_last) < 1.5 and abs(fast_prev - slow_prev) < 1.5:
            return ("Echo Sync Flat", 1.0)
        elif fast_last > slow_last and fast_prev > slow_prev:
            return ("Echo Sync Up", 1.5)
        elif fast_last < slow_last and fast_prev < slow_prev:
            return ("Echo Sync Down", 1.5)
        elif fast_last < 20 and fast_prev < 30 and slow_last < 30:
            return ("Echo Collapse Bearish", 1.8)
        elif fast_last > 80 and fast_prev > 70 and slow_last > 70:
            return ("Echo Collapse Bullish", 1.8)

        return ("None", 0.0)
    except Exception as e:
        print("[Echo Engine ERROR]", e)
        return ("Error", 0.0)

# --- Full Multi-Timeframe Echo Analyzer ---
def get_multi_tf_echo_signals(tf_data_map):
    report = {}
    total_score = 0
    total_frames = 0

    for tf, df in tf_data_map.items():
        signal, score = detect_echo_vsplit(df)
        report[tf] = {"status": signal, "strength": score}
        if signal != "None" and signal != "Error":
            total_score += score
            total_frames += 1

    average_score = round(total_score / total_frames, 2) if total_frames else 0.0
    return report, average_score
