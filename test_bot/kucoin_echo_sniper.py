# kucoin_echo_sniper.py
# KuCoin Echo V Sniper with Multi-Timeframe AI Analysis

from kucoin_feed import get_multi_tf_kucoin_data
from echo_v_engine import get_multi_tf_echo_signals
from discord_alert import send_discord_alert
from datetime import datetime
import numpy as np

print("[TEST LOOP] 🧪 Starting KuCoin Echo V Test Bot...")

def run_kucoin_test():
    try:
        print("[TEST LOOP] 🔁 New Test Cycle")

        tf_data_map = get_multi_tf_kucoin_data()
        if not tf_data_map:
            print("[KUCOIN TEST] No data returned.")
            return

        echo_results = get_multi_tf_echo_signals(tf_data_map)
        tf_summary = echo_results.get("summary", [])
        primary_signal = echo_results.get("primary", {})

        df_1m = tf_data_map["1m"]
        close_prices = df_1m['close'].astype(float).tolist()
        last_close = float(close_prices[-1])
        vwap = float(df_1m['vwap'].iloc[-1]) if 'vwap' in df_1m.columns else np.mean(close_prices)
        rsi = float(df_1m['rsi'].iloc[-1])
        volume = df_1m['volume'].astype(float).tolist()

        # Mock spoof ratio for now
        spoof_ratio = round(volume[-1] / (np.mean(volume[-10:]) + 1e-5), 3)

        trap = {
            "symbol": "BTC/USDT",
            "exchange": "KuCoin Test",
            "timestamp": datetime.utcnow().isoformat(),
            "entry_price": last_close,
            "vwap": round(vwap, 2),
            "rsi": round(rsi, 2),
            "spoof_ratio": spoof_ratio,
            "bias": "Below" if last_close < vwap else "Above",
            "trap_type": "Echo V Only",
            "rsi_status": primary_signal.get("status", "None"),
            "score": primary_signal.get("strength", 0.0),
            "confidence": primary_signal.get("strength", 0.0),
            "reasons": [primary_signal.get("status", "None")],
            "vsplit_score": "N/A",
            "macro_vsplit": [],
            "macro_biases": [],
            "echo_tf_summary": tf_summary
        }

        send_discord_alert(trap)

    except Exception as e:
        print(f"[KUCOIN TEST ERROR] {e}")
