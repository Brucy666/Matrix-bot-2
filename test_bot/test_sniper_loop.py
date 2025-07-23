import time
from kucoin_echo_sniper import run_echo_sniper

print("[TEST LOOP] Running Echo RSI Bot...")

while True:
    try:
        run_echo_sniper()
    except Exception as e:
        print("[TEST ERROR]", e)

    time.sleep(60)
