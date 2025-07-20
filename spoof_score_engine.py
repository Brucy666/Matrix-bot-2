# spoof_score_engine.py
# Enhances sniper trap data with Binance spoof ratio and wall logic

from binance_feed import analyze_binance_spoof

def apply_binance_spoof_scoring(trap):
    spoof_data = analyze_binance_spoof(symbol="BTCUSDT")

    spoof_ratio = spoof_data.get("spoof_ratio", 0.0)
    bid_wall = spoof_data.get("bid_wall", 0.0)
    ask_wall = spoof_data.get("ask_wall", 0.0)

    trap["spoof_ratio"] = spoof_ratio
    trap["binance_bid_wall"] = bid_wall
    trap["binance_ask_wall"] = ask_wall

    # Simple logic: score bump if spoof ratio > 1.5 and large bid wall exists
    if spoof_ratio > 1.5 and bid_wall > 100:
        trap["score"] += 0.5
        trap["reasons"].append("Binance Spoof Confirmed")

    return trap

if __name__ == "__main__":
    sample_trap = {
        "symbol": "BTC/USDT",
        "entry_price": 58250.0,
        "vwap": 58300.0,
        "rsi": 33.5,
        "score": 2.0,
        "reasons": ["RSI-V", "VWAP Rejection"]
    }

    updated = apply_binance_spoof_scoring(sample_trap)
    print("[SPOOF SCORE UPDATED]", updated)
