# btc_sniper_engine.py

from kucoin_feed import get_kucoin_sniper_feed, fetch_orderbook
from rsi_vsplit_engine import detect_rsi_vsplit
from multi_tf_vsplit_engine import scan_multi_tf_rsi
from spoof_score_engine import apply_binance_spoof_scoring
from trap_journal import log_sniper_event
from discord_alert import send_discord_alert
from datetime import datetime
import numpy as np

print("[✓] BTC Sniper Engine Started for BTC-USDT...")

def run_btc_sniper():
    df = get_kucoin_sniper_feed()
    if df is None or len(df) < 20:
        print("[BTC SNIPER] No data returned from KuCoin feed.")
        return

    try:
        close_prices = df['close'].astype(float).tolist()
        rsi_series = df['rsi'].astype(float).tolist()
        volume = df['volume'].astype(float).tolist()

        last_close = float(close_prices[-1])
        vwap = float(df['vwap'].iloc[-1]) if 'vwap' in df.columns else np.mean(close_prices)

        orderbook = fetch_orderbook()
        bids = float(orderbook.get("bids", 1.0))
        asks = float(orderbook.get("asks", 1.0))

        # Compute fast and slow RSI
        fast_rsi = rsi_series
        slow_rsi = df['rsi'].rolling(8).mean().fillna(50).astype(float).tolist()

        # Detect primary RSI-V signal
        vsplit = detect_rsi_vsplit(fast_rsi, slow_rsi)

        # Retrieve macro V-Split summary
        macro_summary, macro_bias = scan_multi_tf_rsi()

        # Trap payload
        trap = {
            "symbol": "BTC/USDT",
            "exchange": "KuCoin",
            "timestamp": datetime.utcnow().isoformat(),
            "entry_price": last_close,
            "vwap": round(vwap, 2),
            "rsi": round(rsi_series[-1], 2),
            "score": vsplit["strength"],
            "reasons": [vsplit["reason"]] if vsplit["reason"] else ["No V-Split"],
            "trap_type": vsplit["type"] if vsplit["type"] else "VWAP Trap",
            "spoof_ratio": round(bids / asks, 2) if asks else 0,
            "bias": "Below" if last_close < vwap else "Above",
            "confidence": round(vsplit["strength"], 1),
            "rsi_status": vsplit["type"] if vsplit["type"] else "None",
            "vsplit_score": "VWAP Zone" if abs(last_close - vwap) / vwap < 0.002 else "Outside Range",
            "macro_vsplit": [f"{s['timeframe']}: {s['type']} ({s['strength']})" for s in macro_summary],
            "macro_biases": [macro_bias]
        }

        # Adjust confidence using macro bias
        if macro_bias == "Strong Bull":
            trap["confidence"] += 2
        elif macro_bias == "Strong Bear":
            trap["confidence"] -= 1

        # Add spoof scoring
        trap = apply_binance_spoof_scoring(trap)

        # Log and send alert
        log_sniper_event(trap)
        send_discord_alert(trap)

        if trap["score"] >= 2:
            print("[TRIGGER] KuCoin Sniper Entry:", trap)
        else:
            print(f"[BTC SNIPER] No trap. Score: {trap['score']}, RSI: {rsi_series[-1]}, Price: {last_close}")

    except Exception as e:
        print(f"[!] BTC Sniper Error: {e}")
