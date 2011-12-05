from matplotlib import finance, mlab
import numpy
import datetime
import time

symbol = 'AAPL'

start = datetime.date(2006, 11, 30)
end = datetime.date(2011, 12, 2)
answer = 0

# Catch CSV
stock_history = finance.fetch_historical_yahoo(symbol, start, end)

# From CSV to REACARRAY
r = mlab.csv2rec(stock_history)
