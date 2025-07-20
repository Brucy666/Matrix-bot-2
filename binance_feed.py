# binance_feed.py
import requests
import pandas as pd

BINANCE_BASE_URL = "https://api.binance.com"

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

        # RSI calculation (14-period)
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
