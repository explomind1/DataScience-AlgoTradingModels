import yfinance


yahoo_data = yfinance.Ticker("AAPL")
print(yahoo_data.info)