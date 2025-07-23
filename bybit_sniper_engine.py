# bybit_sniper_engine.py
# Sniper logic for BTC/USDT using Bybit data with Echo V detection

from bybit_feed import get_bybit_sniper_feed
from kucoin_feed import fetch_orderbook  # used for orderbook spoof scoring
from sniper_score import score_vsplit_vwap
from echo_v_engine import detect_echo_v
from spoof_score_engine import apply_binance_spoof_scoring
from trap_journal import log_sniper_event
from discord_alert import send_discord_alert
from datetime import datetime
import numpy as np

print("[✓] Bybit Sniper Engine Started for BTC-USDT...")

def run_bybit_sniper():
    df = get_bybit_sniper_feed()
    if df is None or len(df) < 20:
        print("[BYBIT SNIPER] No data received from Bybit.")
        return

    try:
        # Market data
        close_prices = df['close'].astype(float).tolist()
        rsi_series = df['rsi'].astype(float).tolist()
        volume = df['volume'].astype(float).tolist()
        last_close = float(close_prices[-1])
        vwap = float(df['vwap'].iloc[-1]) if 'vwap' in df.columns else np.mean(close_prices)

        # Orderbook spoof ratio (from KuCoin feed for now)
        orderbook = fetch_orderbook()
        bids = float(orderbook.get("bids", 1.0))
        asks = float(orderbook.get("asks", 1.0))

        # Scoring
        score, reasons = score_vsplit_vwap({
            "rsi": rsi_series,
            "price": last_close,
            "vwap": vwap,
            "bids": bids,
            "asks": asks
        })

        # Echo V detection
        echo_signal = detect_echo_v(df)
        if echo_signal:
            reasons.append(f"Echo V: {echo_signal}")

        # Trap object
        trap = {
            "symbol": "BTC/USDT",
            "exchange": "Bybit",
            "timestamp": datetime.utcnow().isoformat(),
            "entry_price": last_close,
            "vwap": round(vwap, 2),
            "rsi": round(rsi_series[-1], 2),
            "score": score,
            "confidence": round(score, 1),
            "reasons": reasons,
            "trap_type": "RSI-V + VWAP Trap",
            "spoof_ratio": round(bids / asks, 2) if asks else 0,
            "bias": "Below" if last_close < vwap else "Above",
            "rsi_status": "V-Split" if score >= 2 else "None",
            "vsplit_score": "VWAP Zone" if abs(last_close - vwap) / vwap < 0.002 else "Outside Range",
            "macro_vsplit": [],
            "macro_biases": [],
            "echo_v": echo_signal or "None"
        }

        trap = apply_binance_spoof_scoring(trap)
        log_sniper_event(trap)
        send_discord_alert(trap)

        if trap["score"] >= 2:
            print("[TRIGGER] Bybit Sniper Entry:", trap)
        else:
            print(f"[BYBIT SNIPER] No trap. Score: {trap['score']}, RSI: {rsi_series[-1]}, Price: {last_close}")

    except Exception as e:
        print(f"[!] Bybit Sniper Error: {e}")
