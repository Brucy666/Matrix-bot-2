import ccxt

exchange = ccxt.binance()
symbol = "BTC/USDT"

ticker = exchange.fetch_ticker(symbol)
ohlcv = exchange.fetch_ohlcv(symbol, timeframe='1m', limit=1)

print("✅ Binance BTC/USDT Ticker:", ticker['last'])
print("✅ Latest 1m Candle:", ohlcv[-1])