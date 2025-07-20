# binance_feed.py
# Pulls L2 depth data from Binance and identifies spoof zones

import requests

BINANCE_URL = "https://api.binance.com"

# Pull order book depth (default: 100 levels)
def fetch_binance_orderbook(symbol="BTCUSDT", limit=100):
    url = f"{BINANCE_URL}/api/v3/depth"
    params = {"symbol": symbol.upper(), "limit": limit}
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        bids = [(float(p), float(q)) for p, q in data.get("bids", [])]
        asks = [(float(p), float(q)) for p, q in data.get("asks", [])]
        return bids, asks
    except Exception as e:
        print(f"[!] Binance orderbook error: {e}")
        return [], []

# Analyze spoof zones and return spoof score
def analyze_binance_spoof(symbol="BTCUSDT"):
    bids, asks = fetch_binance_orderbook(symbol)
    if not bids or not asks:
        return {
            "spoof_ratio": 0.0,
            "bid_wall": 0.0,
            "ask_wall": 0.0
        }

    total_bids = sum(q for _, q in bids)
    total_asks = sum(q for _, q in asks)
    spoof_ratio = round(total_bids / total_asks, 3) if total_asks else 0.0
    bid_wall = max(bids, key=lambda x: x[1], default=(0, 0))[1]
    ask_wall = max(asks, key=lambda x: x[1], default=(0, 0))[1]

    return {
        "spoof_ratio": spoof_ratio,
        "bid_wall": bid_wall,
        "ask_wall": ask_wall
    }

if __name__ == "__main__":
    result = analyze_binance_spoof("BTCUSDT")
    print("[BINANCE SPOOF]", result)
