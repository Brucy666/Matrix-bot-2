# sniper_loop.py
import time
from btc_sniper_engine import run_btc_sniper
from bybit_sniper_engine import run_bybit_sniper
from dotenv import load_dotenv
import os

load_dotenv()

print("[LOOP] Starting sniper loop...")

while True:
    print("[LOOP] Running KuCoin sniper...")
    run_btc_sniper()

    print("[LOOP] Running Bybit sniper...")
    run_bybit_sniper()

    time.sleep(60)  # Run every 60 seconds
