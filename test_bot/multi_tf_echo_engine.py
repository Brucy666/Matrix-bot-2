# multi_tf_echo_engine.py
# Multi-timeframe Echo V Signal Aggregator for KuCoin

from echo_v_engine import detect_echo_vsplit

# ---- Timeframes to Process ----
TF_LIST = ["4h", "1h", "30m", "15m", "6m", "3m"]

# ---- Main Aggregator ----
def get_multi_tf_echo_signals(tf_data_map: dict) -> dict:
    results = []

    for tf in TF_LIST:
        df = tf_data_map.get(tf)
        if df is None or len(df) < 20:
            results.append({"tf": tf, "signal": "Missing", "strength": 0.0})
            continue

        try:
            signal = detect_echo_vsplit(df)
            results.append({
                "tf": tf,
                "signal": signal.get("status", "None"),
                "strength": round(signal.get("strength", 0.0), 2)
            })
        except Exception as e:
            results.append({"tf": tf, "signal": "Error", "strength": 0.0})
            print(f"[ECHO {tf} ERROR]", e)

    # ---- Final Decision Logic ----
    vote_counter = {}
    for r in results:
        s = r["signal"]
        if s not in vote_counter:
            vote_counter[s] = 0
        vote_counter[s] += 1

    dominant_signal = max(vote_counter, key=vote_counter.get, default="None")
    avg_strength = round(sum(r["strength"] for r in results if r["signal"] == dominant_signal) / max(1, vote_counter[dominant_signal]), 2)

    return {
        "echo_summary": results,
        "dominant_signal": dominant_signal,
        "avg_strength": avg_strength
    }
