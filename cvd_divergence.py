# cvd_divergence.py

def detect_cvd_divergence(price_series, cvd_series):
    """
    Detects simple bullish or bearish divergence between price and CVD series.
    Returns a dict with status and direction if divergence is detected.
    """
    if len(price_series) < 10 or len(cvd_series) < 10:
        return {"divergence": False, "direction": None, "reason": "insufficient data"}

    try:
        price_high_1 = max(price_series[-10:-5])
        price_high_2 = max(price_series[-5:])
        cvd_high_1 = max(cvd_series[-10:-5])
        cvd_high_2 = max(cvd_series[-5:])

        price_low_1 = min(price_series[-10:-5])
        price_low_2 = min(price_series[-5:])
        cvd_low_1 = min(cvd_series[-10:-5])
        cvd_low_2 = min(cvd_series[-5:])

        # Bearish divergence: price higher high, CVD lower high
        if price_high_2 > price_high_1 and cvd_high_2 < cvd_high_1:
            return {"divergence": True, "direction": "bearish", "reason": "Bearish CVD Divergence"}

        # Bullish divergence: price lower low, CVD higher low
        if price_low_2 < price_low_1 and cvd_low_2 > cvd_low_1:
            return {"divergence": True, "direction": "bullish", "reason": "Bullish CVD Divergence"}

        return {"divergence": False, "direction": None, "reason": "No divergence"}

    except Exception as e:
        return {"divergence": False, "direction": None, "reason": f"CVD error: {e}"}
