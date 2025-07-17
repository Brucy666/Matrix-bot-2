import vectorbt as vbt
import numpy as np

# Download historical BTC data from Yahoo
price = vbt.YFData.download("BTC-USD", period="7d").get("Close")

# ✅ Create random boolean entries (True/False)
entries = np.random.choice([True, False], size=price.shape)
exits = np.roll(entries, 5)  # exit 5 candles later

# Build portfolio
pf = vbt.Portfolio.from_signals(price, entries, exits)

# Show backtest chart
pf.plot().show()