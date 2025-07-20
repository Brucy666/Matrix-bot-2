# rsi_vsplit_engine.py
# Detects bullish and bearish RSI V-Splits from raw RSI data

def detect_rsi_vsplit(fast: list, slow: list) -> dict:
    if not fast or not slow or len(fast) < 4 or len(slow) < 4:
        return {"type": None, "strength": 0, "reason": None}

    f0, f1, f2 = fast[-3:]
    s0, s1, s2 = slow[-3:]

    # Bullish V-Split: Fast dips then recovers, slow holds up
    if f1 < f0 and f2 > f1 and s2 >= s1 >= s0:
        strength = round(abs(s2 - f1), 2)
        return {
            "type": "Bullish V-Split",
            "strength": strength,
            "reason": f"Fast dipped to {round(f1)} while Slow held {round(s2)}"
        }

    # Bearish V-Split: Fast spikes then reverses, slow stays low
    if f1 > f0 and f2 < f1 and s2 <= s1 <= s0:
        strength = round(abs(f1 - s2), 2)
        return {
            "type": "Bearish V-Split",
            "strength": strength,
            "reason": f"Fast peaked at {round(f1)} while Slow stayed near {round(s2)}"
        }

    return {"type": None, "strength": 0, "reason": None}
