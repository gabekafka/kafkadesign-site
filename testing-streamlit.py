import yfinance as yf

# 1) Create a Ticker object
ticker = yf.Ticker("AAPL")

# 2) Get historical market data
hist = ticker.history(period="1mo", interval="1d")  # 1 month of daily data

print(hist.head())