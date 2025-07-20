# macro_vsplit_engine.py

import pandas as pd
import numpy as np

def calculate_rsi(close, period=14):
    delta = close.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = -delta.clip(upper=0).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def detect_vsplit(rsi_series):
    if len(rsi_series) < 3:
        return False, 0.0

    rsi1, rsi2, rsi3 = rsi_series[-3], rsi_series[-2], rsi_series[-1]

    if rsi1 > rsi2 < rsi3 and rsi3 > 30:
        split_strength = abs(rsi1 - rsi2) + abs(rsi3 - rsi2)
        return True, round(split_strength / 2, 2)
    
    return False, 0.0

def macro_vsplit_engine(rsi_dict):
    """
    Input:
    {
        "12h": pd.Series,
        "4h": pd.Series,
        "2h": pd.Series,
        "1h": pd.Series
    }
    Output:
    {
        "macro_vsplit": {
            "12h": {"vsplit": True, "strength": 3.2},
            ...
            "score": 7.9,
            "bias": "bearish"
        }
    }
    """
    macro_result = {}
    total_score = 0.0
    trigger_count = 0

    for tf, rsi_series in rsi_dict.items():
        vsplit, strength = detect_vsplit(rsi_series)
        macro_result[tf] = {"vsplit": vsplit, "strength": strength if vsplit else 0.0}
        if vsplit:
            total_score += strength
            trigger_count += 1

    macro_result["score"] = round(total_score, 2)
    macro_result["bias"] = "bearish" if trigger_count >= 2 else "neutral"

    return {"macro_vsplit": macro_result}
