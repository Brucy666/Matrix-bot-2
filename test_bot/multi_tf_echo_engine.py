# multi_tf_echo_engine.py
# Multi-timeframe Echo V AI Engine for KuCoin Test Bot

from echo_v_engine import detect_echo_vsplit

# Define timeframes to scan
ECHO_TIMEFRAMES = ["1m", "5m", "15m", "1h", "4h"]

# Analyze Echo pattern on each timeframe's dataframe
def get_multi_tf_echo_signals(tf_data_map: dict) -> dict:
    results = {}
    try:
        for tf, df in tf_data_map.items():
            echo = detect_echo_vsplit(df)
            results[tf] = echo
    except Exception as e:
        print("[ECHO MULTI-TF ERROR]", e)
    return results

# Score confluence across all timeframes
def score_echo_confluence(echo_results: dict) -> dict:
    try:
        matched = []
        confidence = 0.0

        for tf, result in echo_results.items():
            status = result.get("status", "None")
            strength = result.get("strength", 0.0)

            if status != "None":
                matched.append(f"{tf}: {status} ({strength})")
                confidence += strength * 0.25  # Weight TF strength

        bias = "Bullish" if any("Bullish" in x for x in matched) else ("Bearish" if any("Bearish" in x for x in matched) else "Neutral")

        return {
            "summary": matched,
            "bias": bias,
            "confidence": round(confidence, 2)
        }
    except Exception as e:
        print("[ECHO CONFLUENCE ERROR]", e)
        return {
            "summary": [],
            "bias": "Error",
            "confidence": 0.0
        }
