import requests

# ----------------------------
# Fetch Current Price (Spot)
# ----------------------------
def get_price():
    url = "https://api.binance.com/api/v3/ticker/price"
    params = {"symbol": "BTCUSDT"}
    res = requests.get(url, params=params)
    return float(res.json()['price'])

# ----------------------------
# Fetch Order Book Depth
# ----------------------------
def get_order_book():
    url = "https://api.binance.com/api/v3/depth"
    params = {"symbol": "BTCUSDT", "limit": 5}
    res = requests.get(url, params=params)
    data = res.json()
    return data['bids'], data['asks']

# ----------------------------
# Run the Test
# ----------------------------
if __name__ == "__main__":
    print("🔄 Testing Binance BTC/USDT Spot Feed...\n")

    try:
        price = get_price()
        print(f"✅ Current BTC/USDT Price: ${price:,.2f}\n")

        bids, asks = get_order_book()

        print("📉 Top 5 Bids:")
        for bid in bids:
            print(f"  {bid[1]} BTC @ ${bid[0]}")

        print("\n📈 Top 5 Asks:")
        for ask in asks:
            print(f"  {ask[1]} BTC @ ${ask[0]}")

    except Exception as e:
        print("❌ Error fetching Binance data:", e)
