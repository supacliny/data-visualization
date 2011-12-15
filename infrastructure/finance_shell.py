import datetime
import time
from datavis.stocks import Stocks

symbol = 'EBAY'

start = datetime.date(1999, 12, 31)
end = datetime.datetime.now()

stock = Stocks(symbol, start, end)
dates, prices = stock.get_stock_history()

