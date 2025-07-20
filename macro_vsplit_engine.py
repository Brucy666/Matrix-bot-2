# macro_vsplit_engine.py
# Multi-Timeframe RSI V-Split Detector for BTC/USDT

from datetime import datetime
import numpy as np
import random

# ------------------------------------------
# 🔧 Mock OHLCV Data Generator (Replaceable)
# ------------------------------------------
def generate_mock_ohlcv(length=100):
    prices = np.cumsum(np.random.randn(length) * 20 + 100)
    volumes = np.random.rand(length) * 1000
    return {
        "close": prices,
        "volume": volumes,
        "timestamp": [datetime.utcnow().isoformat()] * length
    }

# -----------------------------
# 📈 RSI Calculator (14-period)
# -----------------------------
def calculate_rsi(prices, period=14):
    delta = np.diff(prices)
    gain = np.maximum(delta, 0)
    loss = -np.minimum(delta, 0)
    avg_gain = np.convolve(gain, np.ones(period), 'valid') / period
    avg_loss = np.convolve(loss, np.ones(period), 'valid') / period
    rs = avg_gain / (avg_loss + 1e-6)
    rsi = 100 - (100 / (1 + rs))
    return np.concatenate((np.full(period - 1, 50), rsi))

# ----------------------------------------
# 🔍 V-Split Detection on RSI Trend Slope
# ----------------------------------------
def detect_rsi_vsplit(rsi_series):
    if len(rsi_series) < 10:
        return False, rsi_series[-1], rsi_series[-2]

    recent = rsi_series[-5:]
    slope = np.polyfit(range(len(recent)), recent, 1)[0]
    return slope > 1.5, rsi_series[-1], rsi_series[-2]

# -----------------------------
# 🧠 Main Macro Detection Engine
# -----------------------------
print("\n[🔍 Macro V-Split Engine Starting...]")

# Simulated timeframes and labels
timeframes = {
    "1m": generate_mock_ohlcv(),
    "5m": generate_mock_ohlcv(),
    "15m": generate_mock_ohlcv(),
    "1h": generate_mock_ohlcv(),
    "4h": generate_mock_ohlcv(),
    "1D": generate_mock_ohlcv()
}

for tf, data in timeframes.items():
    rsi = calculate_rsi(data["close"])
    signal, current, previous = detect_rsi_vsplit(rsi)
    if signal:
        print(f"[✓] {tf} RSI V-Split Detected ➜ RSI: {round(previous,1)} ➔ {round(current,1)}")
    else:
        print(f"[ ] {tf} No V-Split ➜ RSI: {round(current,1)}")

print("[✓] Macro V-Split Engine Complete\n")
