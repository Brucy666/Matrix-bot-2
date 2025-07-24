# test_bot/kucoin_echo_sniper.py

from kucoin_feed import get_multi_tf_kucoin_data
from echo_v_engine import get_multi_tf_echo_signals
from discord_alert import send_discord_alert
from datetime import datetime

print("[TEST LOOP] 📈 Starting KuCoin Echo V Test Bot...")

def run_kucoin_test():
    try:
        print("[TEST LOOP] 🔄 New Test Cycle")

        # Fetch multi-timeframe KuCoin data
        tf_data = get_multi_tf_kucoin_data()
        if not tf_data:
            print("[KUCOIN TEST] No data returned.")
            return

        # Run Echo AI Engine
        echo_result = get_multi_tf_echo_signals(tf_data)
        if echo_result.get("status") == "Error":
            print("[Echo Engine ERROR]", echo_result.get("reason", "Unknown"))
        
        # Build alert payload
        df_1m = tf_data.get("1m")
        if df_1m is None:
            print("[KUCOIN TEST ERROR] 1m data missing")
            return

        last_row = df_1m.iloc[-1]
        entry_price = float(last_row["close"])
        vwap = round(df_1m["close"].mean(), 2)
        spoof_ratio = 0.0  # Optional: Add orderbook spoofing

        alert = {
            "symbol": "BTC/USDT",
            "exchange": "KuCoin Test",
            "timestamp": datetime.utcnow().isoformat(),
            "entry_price": entry_price,
            "vwap": vwap,
            "rsi": round(last_row["close"], 2),
            "spoof_ratio": round(spoof_ratio, 3),
            "bias": "Below" if entry_price < vwap else "Above",
            "trap_type": "Echo V Only",
            "rsi_status": echo_result.get("status", "None"),
            "score": echo_result.get("strength", 0.0),
            "confidence": echo_result.get("strength", 0.0),
            "reasons": [echo_result.get("status")] if echo_result.get("status") else ["None"],
            "vsplit_score": "N/A",
            "macro_vsplit": [],
            "macro_biases": []
        }

        send_discord_alert(alert)

    except Exception as e:
        print("[KUCOIN TEST ERROR]", e)
