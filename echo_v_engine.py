# echo_v_engine.py
# Echo V Engine – Heikin Ashi RSI Split Detector

import pandas as pd
import numpy as np

# --- Heikin Ashi Candles ---
def heikin_ashi(df):
    ha = pd.DataFrame(index=df.index)
    ha['close'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4
    ha['open'] = df['open']
    ha['high'] = df[['open', 'close', 'high']].max(axis=1)
    ha['low'] = df[['open', 'close', 'low']].min(axis=1)
    return ha

# --- Smoothed RSI ---
def compute_smoothed_rsi(prices, length=14, smooth=2):
    delta = prices.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(length).mean()
    avg_loss = loss.rolling(length).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.rolling(smooth).mean()

# --- Echo V Pattern Detector ---
def get_echo_v_signal(df):
    try:
        ha = heikin_ashi(df)
        close = ha['close']

        fast = compute_smoothed_rsi(close, length=14, smooth=2)
        slow = compute_smoothed_rsi(close, length=14, smooth=8)

        if len(fast) < 2 or len(slow) < 2:
            return {"status": "None", "strength": 0.0}

        fast_last, fast_prev = fast.iloc[-1], fast.iloc[-2]
        slow_last, slow_prev = slow.iloc[-1], slow.iloc[-2]

        # --- Pattern Rules ---
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
        print("[Echo V ERROR]", e)
        return {"status": "Error", "strength": 0.0}
