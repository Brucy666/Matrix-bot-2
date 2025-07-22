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
    if df is None or df.empty or len(df.columns) < 8:
        print("[OKX SNIPER] No data or malformed dataframe from OKX feed.")
        return

    try:
        # Convert to float and extract
        df["close"] = df["close"].astype(float)
        df["volume"] = df["volume"].astype(float)
        close_prices = df["close"].tolist()

        # Custom RSI calculation (smoothed)
        rsi_series = df["close"].rolling(14).apply(
            lambda x: (100 - (100 / (1 + x.pct_change().mean()))) if x.pct_change().mean() else 0
        ).fillna(0).tolist()

        last_close = close_prices[-1]
        rsi_now = rsi_series[-1]

        # Simple VWAP estimate
        vwap = float(np.average(close_prices, weights=df["volume"]))

        # Orderbook data
        bids, asks = fetch_okx_orderbook()
        total_bids = sum(q for _, q in bids)
        total_asks = sum(q for _, q in asks)

        # Run scoring
        score, reasons = score_vsplit_vwap({
            "rsi": rsi_series,
            "price": last_close,
            "vwap": vwap,
            "bids": total_bids,
            "asks": total_asks
        })

        # V-split pattern detection (pass full df as expected)
        vsplit_status = detect_rsi_vsplit(df, rsi_now)
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

        # Add spoof scoring adjustments
        trap = apply_binance_spoof_scoring(trap)

        # Log + alert
        log_sniper_event(trap)
        send_discord_alert(trap)

        if trap["score"] >= 2:
            print("[TRIGGER] OKX Sniper Entry:", trap)
        else:
            print(f"[OKX SNIPER] No trap. Score: {trap['score']}, RSI: {rsi_now}, Price: {last_close}")

    except Exception as e:
        print(f"[!] OKX Sniper Error: {e}")
