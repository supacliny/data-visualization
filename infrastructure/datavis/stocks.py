import matplotlib.finance as finance
import matplotlib.mlab as mlab
import time


class Stocks:
	"""
	A Stocks instantiation is an object with a symbol, start and end dates.

	Parameters
	----------
	symbol: Stock symbol of company
	start: Start datetime
	end: End datetime

	Returns
	-------
	None
	"""
	def __init__(self, symbol, start, end):
		self.symbol = symbol
		self.start = start
		self.end = end


	def get_stock_history(self):
		"""
		Fetches data using matplotlib's yahoo API (undocumented).
		A call to fetch_historical_yahoo returns a CSV file containing tuples:
		[(date, open, close, high, low, volume),...]
		
		Parameters
		----------
		None

		Returns
		-------
		dates: array of historical dates
		prices: array of associated prices on those dates
		"""
		stock_history = finance.fetch_historical_yahoo(self.symbol, self.start, self.end)
		r = mlab.csv2rec(stock_history)
		r.sort()

		dates = r.date
		prices = r.adj_close

		# convert to epoch time for highcharts
		dates = [(int(time.mktime(time.strptime(date.strftime("%Y-%m-%d"), "%Y-%m-%d"))) - time.timezone)*1000 for date in dates]

		return dates, prices
