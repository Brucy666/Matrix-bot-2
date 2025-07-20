# binance_sniper_engine.py
# Binance sniper engine for global spoof/trap signal detection

from binance_feed import analyze_binance_spoof
from sniper_score import score_vsplit_vwap
from trap_journal import log_sniper_event
from discord_alert import send_discord_alert
from datetime import datetime
import numpy as np

print("[✓] Binance Sniper Engine Started for BTC-USDT...")

def run_binance_sniper():
    try:
        # Pull spoof + wall info
        spoof_data = analyze_binance_spoof("BTCUSDT")
        spoof_ratio = spoof_data.get("spoof_ratio", 0.0)
        bid_wall = spoof_data.get("bid_wall", 0.0)
        ask_wall = spoof_data.get("ask_wall", 0.0)

        # Placeholder RSI/VWAP estimation for now (until full feed wired)
        rsi_series = [44.0, 38.5, 41.2]  # mock RSI
        close_price = 58250.0           # placeholder
        vwap = 58320.0                  # placeholder

        score, reasons = score_vsplit_vwap({
            "rsi": rsi_series,
            "price": close_price,
            "vwap": vwap,
            "bids": bid_wall,
            "asks": ask_wall
        })

        trap = {
            "symbol": "BTC/USDT",
            "exchange": "Binance",
            "timestamp": datetime.utcnow().isoformat(),
            "entry_price": close_price,
            "vwap": round(vwap, 2),
            "rsi": round(rsi_series[-1], 2),
            "score": score,
            "reasons": reasons,
            "trap_type": "Global Spoof Signal",
            "spoof_ratio": spoof_ratio,
            "binance_bid_wall": bid_wall,
            "binance_ask_wall": ask_wall,
            "bias": "Below" if close_price < vwap else "Above",
            "confidence": round(score * 1.5, 1),
            "rsi_status": "V-Split" if score >= 2 else "None",
            "vsplit_score": "VWAP Zone" if abs(close_price - vwap) / vwap < 0.002 else "Outside Range"
        }

        if trap["score"] >= 3:
            log_sniper_event(trap)
            send_discord_alert(trap)
            print("[TRIGGER] Binance Global Sniper Entry:", trap)
        else:
            print(f"[BINANCE SNIPER] No trap. Score: {trap['score']}, RSI: {rsi_series[-1]}, Price: {close_price}")

    except Exception as e:
        print(f"[!] Binance Sniper Error: {e}")
