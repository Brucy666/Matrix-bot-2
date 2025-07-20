# rsi_vsplit_engine.py
# Enhanced RSI-V Classifier Engine for Sniper System

# Detects V-Split, Collapse, Compression, Sync signals from fast/slow RSI

def detect_rsi_vsplit(fast_rsi: list, slow_rsi: list) -> dict:
    if len(fast_rsi) < 3 or len(slow_rsi) < 3:
        return {"type": None, "strength": 0, "reason": None}

    f0, f1, f2 = fast_rsi[-3:]
    s0, s1, s2 = slow_rsi[-3:]

    # V-Split (Bullish)
    if f1 < f0 and f2 > f1 and s2 >= s1 >= s0:
        gap = abs(s2 - f1)
        return {
            "type": "RSI V-Split",
            "strength": round(gap, 2),
            "reason": f"Fast dipped to {round(f1)} while Slow held {round(s2)}"
        }

    # V-Split (Bearish)
    if f1 > f0 and f2 < f1 and s2 <= s1 <= s0:
        gap = abs(f1 - s2)
        return {
            "type": "RSI V-Split",
            "strength": round(gap, 2),
            "reason": f"Fast peaked at {round(f1)} while Slow stayed near {round(s2)}"
        }

    # RSI Collapse — both fast and slow dive
    if f2 < f1 < f0 and s2 < s1 < s0:
        return {
            "type": "RSI Collapse",
            "strength": round((f0 - f2 + s0 - s2) / 2, 2),
            "reason": "Fast and Slow collapsing together"
        }

    # RSI Compression — tight flat RSI alignment
    recent_gap = abs(f2 - s2)
    if recent_gap < 3 and abs(f2 - f1) < 2 and abs(s2 - s1) < 2:
        return {
            "type": "RSI Compression",
            "strength": round(3 - recent_gap, 2),
            "reason": "Fast and Slow tightly compressed"
        }

    # RSI Sync Uptrend — both rising
    if f2 > f1 > f0 and s2 > s1 > s0:
        return {
            "type": "RSI Sync Up",
            "strength": round((f2 + s2) / 2, 2),
            "reason": "Fast and Slow aligned upward"
        }

    # RSI Sync Downtrend — both falling
    if f2 < f1 < f0 and s2 < s1 < s0:
        return {
            "type": "RSI Sync Down",
            "strength": round((f2 + s2) / 2, 2),
            "reason": "Fast and Slow aligned downward"
        }

    return {"type": None, "strength": 0, "reason": None}
