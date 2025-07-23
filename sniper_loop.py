# sniper_loop.py

import time
from btc_sniper_engine import run_btc_sniper
from bybit_sniper_engine import run_bybit_sniper
from binance_sniper_engine import run_binance_sniper
from okx_sniper_engine import run_okx_sniper

print("[LOOP 🧠] 🚀 Starting Sniper Loop Engine...")

while True:
    print("\n[LOOP] 🔁 Starting New Sniper Scan Cycle")

    try:
        print("[LOOP] → KuCoin Sniper...")
        run_btc_sniper()
    except Exception as e:
        print(f"[KuCoin ERROR] {e}")

    try:
        print("[LOOP] → Bybit Sniper...")
        run_bybit_sniper()
    except Exception as e:
        print(f"[Bybit ERROR] {e}")

    try:
        print("[LOOP] → Binance Sniper...")
        run_binance_sniper()
    except Exception as e:
        print(f"[Binance ERROR] {e}")

    try:
        print("[LOOP] → OKX Sniper...")
        run_okx_sniper()
    except Exception as e:
        print(f"[OKX ERROR] {e}")

    print("[LOOP] ⏱️ Sleeping for 60 seconds...\n")
    time.sleep(60)
