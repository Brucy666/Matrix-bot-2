# rsi_vsplit_engine.py
# Classic RSI-V Classifier Engine for Sniper System

def detect_rsi_vsplit(fast_rsi: list, slow_rsi: list) -> dict:
    if len(fast_rsi) < 3 or len(slow_rsi) < 3:
        return {"type": None, "strength": 0, "reason": None}

    f0, f1, f2 = fast_rsi[-3:]
    s0, s1, s2 = slow_rsi[-3:]

    # --- V-Split (Bullish)
    if f1 < f0 and f2 > f1 and s2 == s1 >= s0:
        gap = abs(s2 - f1)
        return {
            "type": "RSI V-Split",
            "strength": round(gap, 2),
            "reason": f"Fast dipped to {round(f1)} while Slow held {round(s2)}"
        }

    # --- V-Split (Bearish)
    if f1 > f0 and f2 < f1 and s2 == s1 <= s0:
        gap = abs(f1 - s2)
        return {
            "type": "RSI V-Split",
            "strength": round(gap, 2),
            "reason": f"Fast peaked at {round(f1)} while Slow stayed near {round(s2)}"
        }

    # --- RSI Collapse (both Fast and Slow dive)
    if f0 > f1 > f2 and s0 > s1 > s2:
        return {
            "type": "RSI Collapse",
            "strength": 1.5,
            "reason": "Both Fast and Slow RSI collapsing"
        }

    # --- Compression / Sync Flat
    if abs(f2 - s2) < 1.5 and abs(f1 - s1) < 1.5:
        return {
            "type": "RSI Sync Flat",
            "strength": 1.0,
            "reason": "Fast and Slow RSI staying compressed"
        }

    # --- Sync Up
    if f0 < f1 < f2 and s0 < s1 < s2:
        return {
            "type": "RSI Sync Up",
            "strength": 1.2,
            "reason": "Both Fast and Slow rising together"
        }

    # --- Sync Down
    if f0 > f1 > f2 and s0 > s1 > s2:
        return {
            "type": "RSI Sync Down",
            "strength": 1.2,
            "reason": "Both Fast and Slow falling together"
        }

    return {"type": None, "strength": 0.0, "reason": None}
