import numpy as np

def calculate_rsi_vsplit(rsi_series):
    if len(rsi_series) < 3:
        return 0, "RSI Too Short"

    split = rsi_series[-2] - rsi_series[-3]
    reconverge = rsi_series[-1] - rsi_series[-2]

    if split < -1 and reconverge > 1:
        return 2, "RSI V-Split"
    elif split < -0.5 and reconverge > 0.5:
        return 1, "RSI Mild V"
    return 0, None

def check_vwap_retest(price, vwap):
    distance = abs(price - vwap) / vwap
    if distance < 0.002:
        return 1, "VWAP Reaction Zone"
    return 0, None

def detect_spoof_ratio(bids, asks):
    if asks == 0: return 0, None
    ratio = bids / asks
    if ratio > 2:
        return 2, "Heavy Spoof"
    elif ratio > 1.5:
        return 1, "Spoof Pressure"
    return 0, None

def score_vsplit_vwap(data):
    try:
        score = 0
        reasons = []

        rsi_score, rsi_reason = calculate_rsi_vsplit(data["rsi"])
        if rsi_score:
            score += rsi_score
            reasons.append(rsi_reason)

        vwap_score, vwap_reason = check_vwap_retest(data["price"], data["vwap"])
        if vwap_score:
            score += vwap_score
            reasons.append(vwap_reason)

        spoof_score, spoof_reason = detect_spoof_ratio(data["bids"], data["asks"])
        if spoof_score:
            score += spoof_score
            reasons.append(spoof_reason)

        return (score, reasons)
    except Exception as e:
        print(f"[!] Scoring Error: {e}")
        return None
