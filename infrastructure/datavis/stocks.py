import matplotlib.finance as finance
import matplotlib.mlab as mlab

import time


class Stocks:
	"""this class will attempt to instantiate a stock object"""

	def __init__(self, symbol, start, end):
		# list of dates and stock prices
		self.symbol = symbol
		self.start = start
		self.end = end


	def get_stock_history(self):
		"""given a stock symbol as a string, produces a dictionary of historical data"""

		stock_history = finance.fetch_historical_yahoo(self.symbol, self.start, self.end)
		r = mlab.csv2rec(stock_history)
		r.sort()

		dates = r.date
		prices = r.adj_close
	
		#convert to epoch time for highcharts
		dates = [(int(time.mktime(time.strptime(date.strftime("%Y-%m-%d"), "%Y-%m-%d"))) - time.timezone)*1000 for date in dates]
	
		return dates, prices
