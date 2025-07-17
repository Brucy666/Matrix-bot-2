from py_vollib.black_scholes import black_scholes
from py_vollib.black_scholes.greeks.analytical import delta, gamma, theta, vega

S = 30000     # Spot price
K = 31000     # Strike
t = 7 / 365   # Time to expiry (in years)
r = 0.01      # Risk-free rate
sigma = 0.55  # Implied volatility (55%)

print("✅ BS Call Price:", black_scholes('c', S, K, t, r, sigma))
print("✅ Delta:", delta('c', S, K, t, r, sigma))
print("✅ Gamma:", gamma('c', S, K, t, r, sigma))
print("✅ Vega:", vega('c', S, K, t, r, sigma))