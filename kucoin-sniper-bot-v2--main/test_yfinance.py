import yfinance as yf

dxy = yf.download("DX-Y.NYB", period="7d", interval="1h")
vix = yf.download("^VIX", period="7d", interval="1h")

print("📈 DXY Latest Close:", dxy['Close'].dropna().iloc[-1])
print("📉 VIX Latest Close:", vix['Close'].dropna().iloc[-1])