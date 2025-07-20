import requests
from datetime import datetime, timedelta

KCS_BASE_URL = "https://api.kucoin.com"

# Fetch klines for a given range and interval
def fetch_klines(symbol, interval, limit):
    url = f"{KCS_BASE_URL}/api/v1/market/candles"
    params = {
        "symbol": symbol,
        "type": interval
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json().get("data", [])[:limit]
    except Exception as e:
        print(f"[VWAP] Error fetching klines: {e}")
        return []

# Calculate VWAP from a list of candles
def calc_vwap(candles):
    try:
        sum_pv = 0
        sum_vol = 0
        for candle in candles:
            high, low, close, vol = float(candle[3]), float(candle[4]), float(candle[2]), float(candle[5])
            typical_price = (high + low + close) / 3
            sum_pv += typical_price * vol
            sum_vol += vol
        return round(sum_pv / sum_vol, 2) if sum_vol else None
    except Exception as e:
        print(f"[VWAP] Error calculating VWAP: {e}")
        return None

# Main entry to get daily/weekly/monthly VWAPs
def get_vwap_levels_dynamic(symbol="BTC-USDT"):
    candles_1min = fetch_klines(symbol, "1min", 1440)
    candles_1h = fetch_klines(symbol, "1hour", 168)
    candles_4h = fetch_klines(symbol, "4hour", 180)  # Approx 30 days

    daily = calc_vwap(candles_1min)
    weekly = calc_vwap(candles_1h)
    monthly = calc_vwap(candles_4h)

    return {
        "vwap_daily": daily,
        "vwap_weekly": weekly,
        "vwap_monthly": monthly
    }
