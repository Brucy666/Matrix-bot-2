# btc_sniper_engine.py

from kucoin_feed import get_kucoin_sniper_feed, fetch_orderbook
from echo_v_engine import detect_echo_v
from sniper_score import score_vsplit_vwap
from spoof_score_engine import apply_binance_spoof_scoring
from trap_journal import log_sniper_event
from discord_alert import send_discord_alert
from datetime import datetime
import numpy as np

print("[✓] BTC Sniper Engine (ECHO) Started for BTC-USDT...")

def run_btc_sniper():
    df = get_kucoin_sniper_feed()
    if df is None or len(df) < 20:
        print("[BTC SNIPER] No data returned from KuCoin feed.")
        return

    try:
        close_prices = df['close'].astype(float).tolist()
        volume = df['volume'].astype(float).tolist()
        last_close = float(close_prices[-1])
        vwap = float(df['vwap'].iloc[-1]) if 'vwap' in df.columns else np.mean(close_prices)

        orderbook = fetch_orderbook()
        bids = float(orderbook.get("bids", 1.0))
        asks = float(orderbook.get("asks", 1.0))

        score, reasons = score_vsplit_vwap({
            "price": last_close,
            "vwap": vwap,
            "bids": bids,
            "asks": asks,
            "rsi": df['rsi'].tolist() if 'rsi' in df.columns else []
        })

        # Echo V Safety Check
        required_cols = ['open', 'high', 'low', 'close']
        if all(col in df.columns for col in required_cols) and len(df) > 15:
            echo_status = detect_echo_v(df)
        else:
            echo_status = "Echo Feed Invalid"

        confidence = round(score + (1 if 'Echo' in echo_status else 0), 1)

        trap = {
            "symbol": "BTC/USDT",
            "exchange": "KuCoin",
            "timestamp": datetime.utcnow().isoformat(),
            "entry_price": last_close,
            "vwap": round(vwap, 2),
            "rsi": round(df['rsi'].iloc[-1], 2) if 'rsi' in df.columns else 0,
            "score": score,
            "confidence": confidence,
            "reasons": reasons,
            "trap_type": "RSI-ECHO + VWAP Trap",
            "spoof_ratio": round(bids / asks, 2) if asks else 0,
            "bias": "Below" if last_close < vwap else "Above",
            "rsi_status": echo_status,
            "vsplit_score": "VWAP Zone" if abs(last_close - vwap) / vwap < 0.002 else "Outside Range",
            "macro_vsplit": [],
            "macro_biases": []
        }

        trap = apply_binance_spoof_scoring(trap)
        log_sniper_event(trap)
        send_discord_alert(trap)

        if trap["score"] >= 2:
            print("[TRIGGER] BTC Sniper Entry:", trap)
        else:
            print(f"[BTC SNIPER] No trap. Score: {trap['score']}, RSI: {trap['rsi']}, Price: {last_close}")

    except Exception as e:
        print(f"[!] BTC Sniper Error: {e}")
