# echo_v_engine.py

def detect_echo_vsplit(df):
    try:
        close = df['close'].astype(float)
        rsi = df['rsi'].astype(float)

        fast = rsi.rolling(2).mean()
        slow = rsi.rolling(8).mean()

        fast_last = fast.iloc[-1]
        fast_prev = fast.iloc[-2]
        slow_last = slow.iloc[-1]
        slow_prev = slow.iloc[-2]

        # Pattern Rules
        if fast_prev < slow_prev and fast_last > slow_last:
            return {
                "status": "Echo V-Split Bullish",
                "strength": 2.0,
                "reason": f"Echo flipped up: {round(fast_last,1)} > {round(slow_last,1)}"
            }
        elif fast_prev > slow_prev and fast_last < slow_last:
            return {
                "status": "Echo V-Split Bearish",
                "strength": 2.0,
                "reason": f"Echo flipped down: {round(fast_last,1)} < {round(slow_last,1)}"
            }
        elif abs(fast_last - slow_last) < 1.5 and abs(fast_prev - slow_prev) < 1.5:
            return {
                "status": "Echo Sync Flat",
                "strength": 1.0,
                "reason": "Echo RSI flat & in sync"
            }
        elif fast_last > slow_last and fast_prev > slow_prev:
            return {
                "status": "Echo Sync Up",
                "strength": 1.5,
                "reason": "Echo RSI aligned upward"
            }
        elif fast_last < slow_last and fast_prev < slow_prev:
            return {
                "status": "Echo Sync Down",
                "strength": 1.5,
                "reason": "Echo RSI aligned downward"
            }
        elif fast_last < 20 and slow_last < 30:
            return {
                "status": "Echo Collapse Bearish",
                "strength": 1.8,
                "reason": f"Echo collapse detected ({round(fast_last,1)})"
            }
        elif fast_last > 80 and slow_last > 70:
            return {
                "status": "Echo Collapse Bullish",
                "strength": 1.8,
                "reason": f"Echo peak detected ({round(fast_last,1)})"
            }

        return {"status": "None", "strength": 0.0, "reason": "No echo match"}

    except Exception as e:
        print("[Echo Engine ERROR]", e)
        return {"status": "Error", "strength": 0.0, "reason": str(e)}
