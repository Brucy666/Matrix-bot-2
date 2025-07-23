from kucoin_feed import get_kucoin_sniper_feed, fetch_orderbook
from echo_v_engine import get_echo_v_signal
from discord_alert import send_discord_alert
from datetime import datetime
import numpy as np

print("[TEST BOT] Echo RSI Sniper running on KuCoin...")

def run_echo_sniper():
    df = get_kucoin_sniper_feed()
    if df is None or len(df) < 20:
        print("[TEST BOT] No KuCoin data.")
        return

    close_prices = df['close'].astype(float).tolist()
    volume = df['volume'].astype(float).tolist()
    last_close = close_prices[-1]
    vwap = float(df['vwap'].iloc[-1]) if 'vwap' in df.columns else np.mean(close_prices)

    bids = float(fetch_orderbook().get("bids", 1.0))
    asks = float(fetch_orderbook().get("asks", 1.0))

    echo = get_echo_v_signal(df)
    echo_status = echo.get("status", "None")
    echo_strength = echo.get("strength", 0.0)

    trap = {
        "symbol": "BTC/USDT",
        "exchange": "KuCoin",
        "timestamp": datetime.utcnow().isoformat(),
        "entry_price": last_close,
        "vwap": round(vwap, 2),
        "rsi": round(df['rsi'].iloc[-1], 2),
        "score": echo_strength,
        "confidence": echo_strength,
        "trap_type": echo_status,
        "spoof_ratio": round(bids / asks, 2) if asks else 0,
        "bias": "Below" if last_close < vwap else "Above",
        "rsi_status": echo_status,
        "vsplit_score": "VWAP Zone" if abs(last_close - vwap) / vwap < 0.002 else "Outside Range",
        "macro_vsplit": [],
        "macro_biases": []
    }

    send_discord_alert(trap)
    print("[TEST BOT] Alert sent:", trap)
