# test_bot/test_kucoin_echo_sniper.py

from kucoin_feed import get_kucoin_sniper_feed, fetch_orderbook
from echo_v_engine import detect_echo_vsplit
from discord_alert import send_discord_alert
from datetime import datetime
import numpy as np

def run_kucoin_test():
    df = get_kucoin_sniper_feed()
    if df is None or len(df) < 20:
        print("[KUCOIN TEST] No data returned.")
        return

    try:
        close = df['close'].astype(float).tolist()
        price = float(close[-1])
        vwap = float(df['vwap'].iloc[-1]) if 'vwap' in df.columns else np.mean(close)

        orderbook = fetch_orderbook()
        bids = float(orderbook.get("bids", 1))
        asks = float(orderbook.get("asks", 1))
        spoof = round(bids / asks, 3) if asks else 0.0

        echo = detect_echo_vsplit(df)
        status = echo["status"]
        strength = echo["strength"]

        trap = {
            "symbol": "BTC/USDT",
            "exchange": "KuCoin Test",
            "timestamp": datetime.utcnow().isoformat(),
            "entry_price": price,
            "vwap": round(vwap, 2),
            "rsi": float(df["rsi"].iloc[-1]),
            "spoof_ratio": spoof,
            "bias": "Below" if price < vwap else "Above",
            "trap_type": "Echo V Only",
            "rsi_status": status,
            "score": strength,
            "confidence": strength,
            "reasons": [status],
            "vsplit_score": "N/A",
            "macro_vsplit": [],
            "macro_biases": []
        }

        send_discord_alert(trap)
        print("[✓] Echo V alert sent:", trap)

    except Exception as e:
        print(f"[KUCOIN TEST ERROR] {e}")
        
