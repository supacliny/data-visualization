import numpy as np


class Indicators:
	"""
	An Indicators instantiation is an object containing three algorithms that
	are specific to the stock market in identifying trends.

	Parameters
	----------
	prices: array of historical stock prices

	Returns
	-------
	None
	"""
	def __init__(self, prices):
		# list of stock prices
		self.prices = prices


	def moving_average(self, n, type='simple'):
		"""
		Moving Average (MA): An average of data for a certain number of time periods. 
		It moves because for each calculation, we use the latest x number of time periods data. 
		By definition, a moving average lags the market. An exponentially smoothed moving average 
		(EMA) gives greater weight to the more recent data, in an attempt to reduce the lag.

		Parameters
		----------
		n: number of time periods of data
		type: simple or exponential

		Returns
		-------
		ma: an array of MA prices for that time period
		"""
		prices = np.asarray(self.prices)
		if type=='simple':
			weights = np.ones(n)
		else:
			 weights = np.exp(np.linspace(-1., 0., n))

		weights /= weights.sum()

		ma =  np.convolve(prices, weights, mode='full')[:len(prices)]
		ma[:n] = ma[n]
		return ma


	def moving_average_convergence(self, nslow=26, nfast=12):
		"""
		MACD (Moving Average Convergence/Divergence): An indicator developed by Gerald Appel that is 
		calculated by subtracting the 26-period exponential moving average of a given security from 
		its 12-period exponential moving average. By comparing moving averages, MACD displays trend 
		following characteristics, and by plotting the difference of the moving averages as an oscillator, 
		MACD displays momentum characteristics.

		Parameters
		----------
		nslow: default 12-period exponential MA
		nfast: default 26-period exponential MA

		Returns
		-------
		macd: an array of MACD prices for that time period
		"""
		emaslow = self.moving_average(nslow, type='exponential')
		emafast = self.moving_average(nfast, type='exponential')
		macd = emafast - emaslow
		return macd


	def relative_strength(self, n=14):
		"""
		Relative Strength Index (RSI): RSI is plotted on a vertical scale from 0 to 100. 
		Values above 70 are considered overbought and values below 30, oversold. 
		When prices are over 70 or below 30 and diverge from price action, 
		a warning is given of a possible trend reversal.

		RSI has been decomposed into its basic components: 
		RS, Average Gain and Average Loss. 
		Calculations are based on 14 periods, which is the default suggested. 

		Parameters
		----------
		n: default 14-period

		Returns
		-------
		rsi: an array of RSI prices for that time period
		"""
		deltas = np.diff(self.prices)
		seed = deltas[:n+1]
		up = seed[seed>=0].sum()/n
		down = -seed[seed<0].sum()/n
		rs = up/down
		rsi = np.zeros_like(self.prices)
		rsi[:n] = 100. - 100./(1.+rs)

		for i in range(n, len(self.prices)):
			delta = deltas[i-1]

			if delta>0:
				upval = delta
				downval = 0.
			else:
				upval = 0.
				downval = -delta

			up = (up*(n-1) + upval)/n
			down = (down*(n-1) + downval)/n

			rs = up/down
			rsi[i] = 100. - 100./(1.+rs)

		return rsi