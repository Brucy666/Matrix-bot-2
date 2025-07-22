# okx_sniper_engine.py
# OKX sniper logic using feed test only (no V-split scoring yet)

from okx_feed import get_okx_ohlcv, fetch_okx_orderbook
from discord_alert import send_discord_alert
from datetime import datetime
import numpy as np

print("[✓] OKX Sniper Engine Running...")

def run_okx_sniper():
    df = get_okx_ohlcv()
    if df is None or len(df) < 2:
        print("[OKX] Feed error: No valid OHLCV data.")
        return

    try:
        last_row = df.iloc[-1]
        last_close = float(last_row["close"])
        last_vol = float(last_row["volume"])
        last_ts = str(last_row["timestamp"])

        bids, asks = fetch_okx_orderbook()
        top_bid = bids[0] if bids else (0, 0)
        top_ask = asks[0] if asks else (0, 0)

        print("[OKX] Price:", last_close)
        print("[OKX] Volume:", last_vol)
        print("[OKX] Top Bid:", top_bid)
        print("[OKX] Top Ask:", top_ask)

        # Format dummy trap data for Discord test
        trap = {
            "symbol": "BTC/USDT",
            "exchange": "OKX",
            "score": 1.0,
            "spoof_ratio": round(top_bid[1] / top_ask[1], 3) if top_ask[1] else 0.0,
            "bias": "Below" if last_close < (top_bid[0] + top_ask[0]) / 2 else "Above",
            "trap_type": "Feed Check",
            "rsi_status": "None",
            "confidence": 1.0,
            "vsplit_score": "Feed Only",
            "macro_biases": [],
            "macro_vsplit": []
        }

        send_discord_alert(trap)

    except Exception as e:
        print("[OKX FEED TEST ERROR]", e)

if __name__ == "__main__":
    run_okx_sniper()
