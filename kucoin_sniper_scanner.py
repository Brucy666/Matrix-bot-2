import requests
import time
from datetime import datetime
from sniper_executor import evaluate_and_execute

BASE_URL = "https://api.kucoin.com"

def fetch_usdt_symbols():
    url = f"{BASE_URL}/api/v1/market/allTickers"
    response = requests.get(url)
    if response.status_code != 200:
        return []
    data = response.json().get("data", {}).get("ticker", [])
    return [item['symbol'] for item in data if item['symbol'].endswith('-USDT')]

def fetch_price(symbol):
    url = f"{BASE_URL}/api/v1/market/orderbook/level1?symbol={symbol}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return float(response.json()["data"]["price"])

def fetch_candles(symbol, interval="1min", limit=100):
    url = f"{BASE_URL}/api/v1/market/candles?type={interval}&symbol={symbol}&limit={limit}"
    response = requests.get(url)
    if response.status_code != 200:
        return []
    return response.json().get("data", [])

def calculate_vwap(candles):
    total_volume = 0.0
    vwap_numerator = 0.0
    for candle in candles:
        high = float(candle[3])
        low = float(candle[4])
        close = float(candle[2])
        volume = float(candle[5])
        typical_price = (high + low + close) / 3
        vwap_numerator += typical_price * volume
        total_volume += volume
    return vwap_numerator / total_volume if total_volume else None

def fetch_orderbook(symbol):
    url = f"{BASE_URL}/api/v1/market/orderbook/level2_20?symbol={symbol}"
    response = requests.get(url)
    if response.status_code != 200:
        return {"bids": [], "asks": []}
    data = response.json().get("data", {})
    return {
        "bids": [(float(p), float(s)) for p, s in data.get("bids", [])],
        "asks": [(float(p), float(s)) for p, s in data.get("asks", [])]
    }

def spoof_score(orderbook):
    if not orderbook["bids"] or not orderbook["asks"]:
        return 0
    total_bid = sum(size for _, size in orderbook["bids"])
    total_ask = sum(size for _, size in orderbook["asks"])
    top_bid = orderbook["bids"][0][1]
    top_ask = orderbook["asks"][0][1]
    if total_bid == 0 or total_ask == 0:
        return 0
    return max(top_bid / total_bid, top_ask / total_ask)

def score_token(symbol):
    try:
        price = fetch_price(symbol)
        candles = fetch_candles(symbol)
        if not candles:
            return None
        vwap = calculate_vwap(candles)
        if not vwap:
            return None
        orderbook = fetch_orderbook(symbol)
        spoof = spoof_score(orderbook)
        bias = "above" if price > vwap else "below" if price < vwap else "neutral"
        score = 0
        if bias == "below": score += 3
        if spoof > 0.15: score += 4
        volatility = abs(float(candles[0][2]) - float(candles[0][3]))
        if volatility < 0.005 * price: score += 2
        return {
            "symbol": symbol,
            "score": round(score, 2),
            "bias": bias,
            "spoof_ratio": round(spoof, 3),
            "vwap": round(vwap, 5),
            "price": round(price, 5),
            "time": datetime.utcnow().isoformat()
        }
    except:
        return None

def run_sniper_loop():
    symbols = fetch_usdt_symbols()[:25]
    for sym in symbols:
        data = score_token(sym)
        if data:
            evaluate_and_execute(data)
    print("✅ Sniper Loop Complete")

if __name__ == "__main__":
    while True:
        run_sniper_loop()
        time.sleep(60)
print("✅ Sniper Loop Complete")
while True:
    pass  # Replace this with your real logic later
