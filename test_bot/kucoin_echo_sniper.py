# test_bot/kucoin_echo_sniper.py

from kucoin_feed import get_multi_ohlcv
from echo_v_engine import get_multi_tf_echo_signals
from discord_alert import send_discord_alert
from trap_journal import log_sniper_event

from datetime import datetime

def run_kucoin_test():
    print("[TEST LOOP] 🧪 New Test Cycle")

    try:
        tf_data = get_multi_ohlcv("BTC/USDT")
        if tf_data is None:
            print("[KUCOIN TEST] No data returned.")
            return

        echo = get_multi_tf_echo_signals(tf_data)

        trap = {
            "symbol": "BTC/USDT",
            "exchange": "KuCoin Test",
            "timestamp": datetime.utcnow().isoformat(),
            "entry_price": echo["price"],
            "vwap": echo["vwap"],
            "rsi": echo["rsi"],
            "spoof_ratio": echo["spoof"],
            "bias": echo["bias"],
            "trap_type": "Echo V Only",
            "rsi_status": echo["status"],
            "score": echo["score"],
            "confidence": echo["confidence"],
            "reasons": echo["reasons"],
            "vsplit_score": "N/A",
            "macro_vsplit": [],
            "macro_biases": [],
        }

        log_sniper_event(trap)
        send_discord_alert(trap)

    except Exception as e:
        print("[KUCOIN TEST ERROR]", str(e)) 
