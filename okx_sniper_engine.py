# okx_sniper_engine.py
# Simple OKX feed test (no V-Split or scoring logic)

from okx_feed import get_okx_ohlcv, fetch_okx_orderbook
from datetime import datetime

print("[✓] OKX Feed Test Initialized...")

def run_okx_sniper():
    df = get_okx_ohlcv()
    if df is None or len(df) < 2:
        print("[OKX] Feed error: No valid OHLCV data.")
        return

    try:
        last_row = df.iloc[-1]
        print("[OKX] Last Close:", last_row["close"])
        print("[OKX] Last Volume:", last_row["volume"])
        print("[OKX] Timestamp:", last_row["timestamp"])

        bids, asks = fetch_okx_orderbook()
        if bids and asks:
            print("[OKX] Top Bid:", bids[0])
            print("[OKX] Top Ask:", asks[0])
        else:
            print("[OKX] Orderbook data unavailable.")

    except Exception as e:
        print("[OKX FEED TEST ERROR]", e)

if __name__ == "__main__":
    run_okx_sniper()
