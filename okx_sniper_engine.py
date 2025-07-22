# okx_sniper_engine.py
# OKX sniper logic using RSI-V + VWAP trap scoring

from okx_feed import get_okx_ohlcv, fetch_okx_orderbook
from sniper_score import score_vsplit_vwap
from spoof_score_engine import apply_binance_spoof_scoring
from trap_journal import log_sniper_event
from discord_alert import send_discord_alert
from rsi_vsplit_engine import detect_rsi_vsplit
import numpy as np
from datetime import datetime

print("[✓] OKX Sniper Engine Started for BTC-USDT...")

def run_okx_sniper():
    df = get_okx_ohlcv()
    if df is None or len(df) < 20:
        print("[OKX SNIPER] No data returned from OKX feed.")
        return

    try:
        close_prices = df["close"].tolist()
        rsi_series = df["close"].rolling(14).apply(lambda x: (100 - (100 / (1 + x.pct_change().mean())))).fillna(0).tolist()
        vwap = float(np.average(close_prices, weights=df["volume"]))

        last_close = float(close_prices[-1])
        rsi_now = float(rsi_series[-1]) if rsi_series[-1] else 0

        bids, asks = fetch_okx_orderbook()
        total_bids = sum(q for _, q in bids)
        total_asks = sum(q for _, q in asks)

        score, reasons = score_vsplit_vwap({
            "rsi": rsi_series,
            "price": last_close,
            "vwap": vwap,
            "bids": total_bids,
            "asks": total_asks
        })

        vsplit_status = detect_rsi_vsplit(df)
        confidence = round(score + (1 if vsplit_status else 0), 1)

        trap = {
            "symbol": "BTC/USDT",
            "exchange": "OKX",
            "timestamp": datetime.utcnow().isoformat(),
            "entry_price": last_close,
            "vwap": round(vwap, 2),
            "rsi": round(rsi_now, 2),
            "score": score,
            "confidence": confidence,
            "reasons": reasons,
            "trap_type": "RSI-V + VWAP Trap",
            "spoof_ratio": round(total_bids / total_asks, 3) if total_asks else 0,
            "bias": "Below" if last_close < vwap else "Above",
            "rsi_status": vsplit_status or "None",
            "vsplit_score": "VWAP Zone" if abs(last_close - vwap) / vwap < 0.002 else "Outside Range",
            "macro_vsplit": [],
            "macro_biases": []
        }

        trap = apply_binance_spoof_scoring(trap)
        log_sniper_event(trap)
        send_discord_alert(trap)

        if trap["score"] >= 2:
            print("[TRIGGER] OKX Sniper Entry:", trap)
        else:
            print(f"[OKX SNIPER] No trap. Score: {trap['score']}, RSI: {rsi_now}, Price: {last_close}")

    except Exception as e:
        print(f"[!] OKX Sniper Error: {e}")
