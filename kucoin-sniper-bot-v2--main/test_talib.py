import talib
import ccxt
import pandas as pd

binance = ccxt.binance()
data = binance.fetch_ohlcv("BTC/USDT", timeframe='1h', limit=100)
df = pd.DataFrame(data, columns=['time', 'open', 'high', 'low', 'close', 'volume'])

# Calculate indicators
rsi = talib.RSI(df['close'], timeperiod=14)
macd, macdsignal, _ = talib.MACD(df['close'])

# Drop NaNs and get latest valid rows
rsi = pd.Series(rsi).dropna()
macd = pd.Series(macd).dropna()

print("✅ RSI:", rsi.iloc[-1])
print("✅ MACD:", macd.iloc[-1])