from pybit.unified_trading import HTTP

session = HTTP(testnet=False)

def get_price():
    response = session.get_tickers(category="linear", symbol="BTCUSDT")
    return float(response['result']['list'][0]['lastPrice'])

def get_order_book():
    response = session.get_orderbook(category="linear", symbol="BTCUSDT", limit=5)
    return response['result']['b'], response['result']['a']

if __name__ == "__main__":
    print("🔄 Testing Bybit BTC/USDT Feed...\n")

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
        print("❌ Error fetching Bybit data:", e)