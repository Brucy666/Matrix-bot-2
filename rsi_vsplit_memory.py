# rsi_vsplit_memory.py
from rsi_vsplit_engine import detect_rsi_vsplit
from kucoin_feed import get_kucoin_sniper_feed

# Timeframes to scan
V_TIMEFRAMES = {
    "1D": "1d",
    "8H": "8h",
    "4H": "4h",
    "2H": "2h",
    "1H": "1h",
    "30M": "30m"
}

def get_multi_rsi_vsplit(symbol="BTCUSDT"):
    summary = []
    bull_count, bear_count = 0, 0

    for label, tf in V_TIMEFRAMES.items():
        df = get_kucoin_sniper_feed(symbol=symbol, interval=tf)
        if df is None or len(df) < 20: continue

        fast = df['rsi'].astype(float).tolist()
        slow = df['rsi'].rolling(8).mean().fillna(50).astype(float).tolist()

        result = detect_rsi_vsplit(fast, slow)
        if result["type"]:
            summary.append({
                "timeframe": label,
                "type": result["type"],
                "strength": result["strength"],
                "reason": result["reason"]
            })

            if result["type"] == "RSI V-Split" and result["strength"] >= 10:
                bull_count += 1
            elif result["type"] == "RSI Collapse" and result["strength"] >= 8:
                bear_count += 1

    bias = "Strong Bull" if bull_count >= 3 else "Strong Bear" if bear_count >= 3 else "Mixed"
    return summary, bias
