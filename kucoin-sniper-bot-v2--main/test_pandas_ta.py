import pandas as pd
import pandas_ta as ta
import ccxt

# Pull 1m candles from Binance
exchange = ccxt.binance()
data = exchange.fetch_ohlcv("BTC/USDT", timeframe='1m', limit=100)

# Create DataFrame
df = pd.DataFrame(data, columns=['time', 'open', 'high', 'low', 'close', 'volume'])

# ⬅️ Fix datetime index for VWAP to work
df['time'] = pd.to_datetime(df['time'], unit='ms')
df.set_index('time', inplace=True)

# Apply RSI and VWAP
df['RSI'] = ta.rsi(df['close'], length=14)
df['VWAP'] = ta.vwap(df['high'], df['low'], df['close'], df['volume'])

# Show result
print(df.tail())
