# kucoin_echo_sniper.py

from kucoin_feed import get_multi_tf_ohlcv
from echo_v_engine import get_multi_tf_echo_signals
from discord_alert import send_discord_alert

def run_kucoin_test():
    print("[TEST LOOP] 📈 Starting KuCoin Echo V Test Bot...")

    try:
        tf_map = {
            "1m": "1min",
            "5m": "5min",
            "15m": "15min",
            "1h": "1hour",
            "4h": "4hour"
        }

        tf_data_map = {}
        for label, tf in tf_map.items():
            try:
                df = get_multi_tf_ohlcv("BTC/USDT", tf)
                if df is None or len(df) < 10:
                    print(f"[KUCOIN ERROR] Skipped {tf} due to insufficient or missing data.")
                    continue
                tf_data_map[label] = df
            except Exception as e:
                print(f"[KUCOIN ERROR] No data returned for {tf}. Error: {e}")
                continue

        if not tf_data_map or "1m" not in tf_data_map:
            print("[KUCOIN TEST ERROR] Base timeframe data (1m) missing. Cannot compute Echo V.")
            return

        echo_result = get_multi_tf_echo_signals(tf_data_map)

        if echo_result:
            send_discord_alert(echo_result)
        else:
            print("[KUCOIN TEST] No valid Echo V signal this cycle.")

    except Exception as e:
        print(f"[KUCOIN TEST ERROR] {e}")
