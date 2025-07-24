# kucoin_echo_sniper.py

from kucoin_feed import get_multi_ohlcv
from echo_v_engine import get_multi_tf_echo_signals
from trap_journal import log_sniper_event
from discord_alert import send_discord_alert
from datetime import datetime

print("[✓] KuCoin Echo Sniper Bot (Multi-Timeframe) Active...")

def run_kucoin_echo_sniper():
    try:
        # Fetch live KuCoin OHLCV data from all timeframes
        tf_map = get_multi_ohlcv("BTC-USDT")

        if not tf_map or len(tf_map) == 0:
            print("[KUCOIN ECHO] No data from KuCoin.")
            return

        echo = get_multi_tf_echo_signals(tf_map)

        if echo["echo_score"] < 2.0:
            print(f"[KUCOIN ECHO] Low signal. Score: {echo['echo_score']:.2f}")
            return

        trap = {
            "symbol": "BTC/USDT",
            "exchange": "KuCoin",
            "timestamp": datetime.utcnow().isoformat(),
            "entry_price": tf_map["1m"]["close"].iloc[-1],
            "vwap": 0.0,
            "rsi": 0.0,
            "score": echo["echo_score"],
            "confidence": echo["confidence"],
            "reasons": echo["reasons"],
            "trap_type": "Echo V AI Signal",
            "spoof_ratio": 0.0,
            "bias": "Unclassified",
            "rsi_status": echo["label"],
            "vsplit_score": "Multi-TF",
            "macro_vsplit": [],
            "macro_biases": []
        }

        log_sniper_event(trap)
        send_discord_alert(trap)
        print("[TRIGGER] Echo Sniper Fired:", trap)

    except Exception as e:
        print(f"[KUCOIN ECHO ERROR] {e}")
