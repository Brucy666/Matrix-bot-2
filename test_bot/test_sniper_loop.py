# sniper_loop.py

import time
from btc_sniper_engine import run_btc_sniper
from bybit_sniper_engine import run_bybit_sniper
from binance_sniper_engine import run_binance_sniper
from okx_sniper_engine import run_okx_sniper
from kucoin_echo_sniper import run_kucoin_echo_sniper  # 🔁 New Echo V AI Engine

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
        print
