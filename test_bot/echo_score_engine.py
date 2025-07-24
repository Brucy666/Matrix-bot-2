# echo_score_engine.py
# Scoring engine for Echo V AI system

def score_echo_signal(signal_map: dict) -> dict:
    try:
        score = 0.0
        confidence = 0.0
        reasons = []

        # Echo signal breakdown by timeframe
        tf_weights = {
            "1m": 0.5,
            "3m": 0.8,
            "5m": 1.0,
            "15m": 1.5,
            "1h": 2.0,
            "4h": 2.5,
            "1d": 3.0
        }

        signal_types = {
            "Echo V-Split Bullish": 2.5,
            "Echo V-Split Bearish": 2.5,
            "Echo Sync Up": 1.5,
            "Echo Sync Down": 1.5,
            "Echo Collapse Bullish": 2.0,
            "Echo Collapse Bearish": 2.0,
            "Echo Sync Flat": 1.0
        }

        # Loop through signals by timeframe
        for tf, result in signal_map.items():
            signal_type = result.get("status")
            if signal_type and signal_type != "None":
                tf_weight = tf_weights.get(tf, 1.0)
                type_weight = signal_types.get(signal_type, 0.0)
                weighted_score = tf_weight * type_weight
                score += weighted_score
                confidence += tf_weight
                reasons.append(f"{tf}: {signal_type}")

        score = round(score, 2)
        confidence = round(confidence, 2)

        return {
            "echo_score": score,
            "confidence": confidence,
            "reasons": reasons if reasons else ["None"]
        }

    except Exception as e:
        print("[Echo Score ERROR]", e)
        return {
            "echo_score": 0.0,
            "confidence": 0.0,
            "reasons": ["Error"]
        }
