# sniper_loop.py
import time
from btc_sniper_engine import run_btc_sniper
from bybit_sniper_engine import run_bybit_sniper
from binance_sniper_engine import run_binance_sniper

print("[LOOP] 🚀 Starting sniper loop...")

while True:
    print("\n[LOOP] 🔁 TICK — New Sniper Cycle")

    print("[LOOP] Running KuCoin sniper...")
    run_btc_sniper()

    print("[LOOP] Running Bybit sniper...")
    run_bybit_sniper()

    print("[LOOP] Running Binance sniper...")
    run_binance_sniper()

    print("[LOOP] 😴 Sleeping for 60 seconds")
    time.sleep(60)
