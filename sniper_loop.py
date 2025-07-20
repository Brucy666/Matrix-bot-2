import time
from btc_sniper_engine import run_btc_sniper
from bybit_sniper_engine import run_bybit_sniper
from binance_sniper_engine import run_binance_sniper  # add this
from dotenv import load_dotenv
import os

load_dotenv()

print("[LOOP] 🚀 Starting sniper loop...")

while True:
    print("[LOOP] 🔁 TICK — New Sniper Cycle")

    print("[LOOP] 🪙 Running KuCoin/BTC sniper...")
    run_btc_sniper()

    print("[LOOP] 📈 Running Bybit sniper...")
    run_bybit_sniper()

    print("[LOOP] 💹 Running Binance sniper...")
    run_binance_sniper()  # new Binance call

    print("[LOOP] 😴 Sleeping for 60 seconds")
    time.sleep(60)
