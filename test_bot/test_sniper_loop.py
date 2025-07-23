# test_bot/test_sniper_loop.py

import time
from kucoin_echo_sniper import run_kucoin_test

print("[TEST LOOP] 🧪 Starting KuCoin Echo V Test Bot...")

while True:
    print("\n[TEST LOOP] 🔁 New Test Cycle")
    try:
        run_kucoin_test()
    except Exception as e:
        print(f"[TEST ERROR] {e}")
    time.sleep(30)  # Shorter loop for testing
