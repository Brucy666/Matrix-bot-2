# sniper_loop.py
import time
from btc_sniper_engine import run_btc_sniper
from bybit_sniper_engine import run_bybit_sniper
from binance_sniper_engine import run_binance_sniper
from okx_sniper_engine import run_okx_sniper

print("[LOOP 🧠] 🚀 Starting Sniper Loop Engine...")

while True:
    print("\n[LOOP] 🔁 Starting New Sniper Scan Cycle")

    print("[LOOP] → KuCoin Sniper...")
    run_btc_sniper()

    print("[LOOP] → Bybit Sniper...")
    run_bybit_sniper()

    print("[LOOP] → Binance Sniper...")
    run_binance_sniper()

    print("[LOOP] → OKX Sniper...")
    run_okx_sniper()

    print("[LOOP] ⏱️ Sleeping for 60 seconds...\n")
    time.sleep(60)
