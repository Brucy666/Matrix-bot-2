# binance_feed.py
import requests
import pandas as pd

BINANCE_BASE_URL = "https://api.binance.com"

# Primary Binance feed for price/RSI/VWAP
def get_binance_sniper_feed(symbol="BTCUSDT"):
    try:
        url = f"{BINANCE_BASE_URL}/api/v3/klines"
        params = {"symbol": symbol, "interval": "1m", "limit": 100}
        res = requests.get(url, params=params, timeout=5)
        data = res.json()
        df = pd.DataFrame(data, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_volume", "trades", "taker_buy_base",
            "taker_buy_quote", "ignore"
        ])
        df = df.astype(float)
        df["vwap"] = df["quote_volume"] / df["volume"]

        delta = df["close"].diff()
        gain = delta.clip(lower=0).rolling(window=14).mean()
        loss = -delta.clip(upper=0).rolling(window=14).mean()
        rs = gain / loss
        df["rsi"] = 100 - (100 / (1 + rs))
        df["rsi"] = df["rsi"].fillna(50)

        return df.tail(20)
    except Exception as e:
        print(f"[!] Binance Feed Error: {e}")
        return None

# Orderbook pull for spoof ratio
def fetch_orderbook(symbol="BTCUSDT"):
    try:
        url = f"{BINANCE_BASE_URL}/api/v3/depth"
        params = {"symbol": symbol, "limit": 100}
        res = requests.get(url, params=params, timeout=5)
        orderbook = res.json()
        bids = sum(float(b[1]) for b in orderbook.get("bids", []))
        asks = sum(float(a[1]) for a in orderbook.get("asks", []))
        return {"bids": bids, "asks": asks}
    except Exception as e:
        print(f"[!] Binance Orderbook Error: {e}")
        return {"bids": 1.0, "asks": 1.0}

# Spoof wall scoring used by spoof_score_engine
def analyze_binance_spoof(symbol="BTCUSDT"):
    try:
        url = f"{BINANCE_BASE_URL}/api/v3/depth"
        params = {"symbol": symbol.upper(), "limit": 100}
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        bids = [(float(p), float(q)) for p, q in data.get("bids", [])]
        asks = [(float(p), float(q)) for p, q in data.get("asks", [])]
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
    except Exception as e:
        print(f"[!] Binance Spoof Analysis Error: {e}")
        return {
            "spoof_ratio": 0.0,
            "bid_wall": 0.0,
            "ask_wall": 0.0
        }
