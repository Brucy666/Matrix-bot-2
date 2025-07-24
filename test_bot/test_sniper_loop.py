# test_sniper_loop.py

import os
import time
from kucoin_echo_sniper import run_kucoin_test

# ✅ Bot Toggle
if os.getenv("BOT_ACTIVE", "true").lower() != "true":
    print("[⏸️ BOT PAUSED] BOT_ACTIVE is false. Exiting sniper loop.")
    exit()

print("[TEST LOOP] 📈 Starting KuCoin Echo V Test Bot...")

while True:
    print("[TEST LOOP] 🔁 New Test Cycle")
    try:
        run_kucoin_test()
    except Exception as e:
        print("[KUCOIN TEST ERROR]", str(e))

    time.sleep(30)
