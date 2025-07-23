# echo_v_engine.py

def get_echo_v_signal(df):
    """
    Basic Echo V Detector using fast vs slow RSI behavior.
    Returns a dictionary with signal type and confidence boost.
    """
    try:
        fast_rsi = df['rsi'].astype(float).rolling(2).mean().tolist()
        slow_rsi = df['rsi'].astype(float).rolling(8).mean().tolist()

        if len(fast_rsi) < 2 or len(slow_rsi) < 2:
            return {"status": "None", "strength": 0.0}

        last_fast = fast_rsi[-1]
        last_slow = slow_rsi[-1]

        if last_fast > last_slow and abs(last_fast - last_slow) > 2:
            return {"status": "Echo Up", "strength": 1.0}
        elif last_fast < last_slow and abs(last_fast - last_slow) > 2:
            return {"status": "Echo Down", "strength": 1.0}
        else:
            return {"status": "None", "strength": 0.0}

    except Exception as e:
        print(f"[Echo V ERROR] {e}")
        return {"status": "None", "strength": 0.0}
