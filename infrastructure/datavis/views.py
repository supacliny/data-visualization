from django.template import RequestContext, loader
from datavis.models import Data
from datavis.stocks import Stocks
from datavis.indicators import Indicators
from datavis.predictors import Predictors
from datavis.transforms import Transforms
from datavis.filters import Filters
from django.http import HttpResponse
from django.views.generic.simple import direct_to_template
import numpy
import datetime
import time


"""
In Django, requests for URLs are mapped to functions in here.
A request for / will be mapped to index(request) and so on.
"""


def index(request):
	"""
	Executed when a request for / comes in. The default symbol is 'EBAY'.
	The default time range is 2000 to now.

	Parameters
	----------
	request: incoming request

	Returns
	-------
	context: data needed for template index.html to render
	"""
	symbol = ""

	if request.method == "POST":
		symbol = request.POST.get("symbol")

	if symbol == "":
		symbol = 'EBAY'

	start = datetime.date(1999, 12, 31)
	end = datetime.datetime.now()

	# get the stock history for that symbol with start and end dates
	stock = Stocks(symbol, start, end)
	try:
		dates, prices = stock.get_stock_history()
	except Exception as e:
		symbol = 'EBAY'
		stock = Stocks(symbol, start, end)
		dates, prices = stock.get_stock_history()

	# find the MA and MACD of this time series
	indicators = Indicators(prices)	
	ma20 = indicators.moving_average(20, type='simple')
	macd = indicators.moving_average_convergence()
	rsi = indicators.relative_strength()

	template = 'datavis/index.html'

	context = {
		'symbol': symbol,
		'dates': dates,
		'prices': prices,
		'ma20': ma20,
		'macd': macd,
		'rsi': rsi,
	}

	return direct_to_template(request, template, context)


def predict(request, symbol):
	"""
	Executed when a request for /predict/SYMBOL comes in.
	Django handles parsing this string for SYMBOL.
	The default time range is 2000 to now.

	Parameters
	----------
	request: incoming request
	symbol: stock symbol

	Returns
	-------
	projection: data needed for "projection" div in index.html to show a next-day stock price via ajax
	"""
	# find the next day stock price in this time series
	start = datetime.date(1999, 12, 31)
	end = datetime.datetime.now()

	# get the stock history for that symbol with start and end dates
	stock = Stocks(symbol, start, end)
	dates, prices = stock.get_stock_history()

	# use our neural network to predict the next day closing price
	predictor = Predictors(dates, prices)
	projection = predictor.predict()
	projection = "%.2f" % projection

	return HttpResponse(projection, mimetype="text/html")
	

def fft(request, symbol):
	"""
	Executed when a request for /fft/SYMBOL comes in.
	Django handles parsing this string for SYMBOL.
	The default time range is 2000 to now.

	Parameters
	----------
	request: incoming request
	symbol: stock symbol

	Returns
	-------
	context: data needed for template fft.html to render
	"""
	# get the stock history for that symbol with start and end dates
	start = datetime.date(1999, 12, 31)
	end = datetime.datetime.now()
	stock = Stocks(symbol, start, end)
	dates, prices = stock.get_stock_history()

	# transform the time-series to the frequency domain
	transform = Transforms(prices)
	period, power = transform.fft2()

	# reverse the numpy array
	period = period[::-1]
	power = power[::-1]

	template = 'datavis/fft.html'

	context = {
		'symbol': symbol,
		'period': period,
		'power': power,
	}

	return direct_to_template(request, template, context)


def kalman(request, symbol):
	"""
	Executed when a request for /kalman/SYMBOL comes in.
	Django handles parsing this string for SYMBOL.
	The default time range is 2000 to now.

	Parameters
	----------
	request: incoming request
	symbol: stock symbol

	Returns
	-------
	context: data needed for template kalman.html to render
	"""
	# get the stock history for that symbol with start and end dates
	start = datetime.date(1999, 12, 31)
	end = datetime.datetime.now()
	stock = Stocks(symbol, start, end)
	dates, prices = stock.get_stock_history()

	#get the mean and standard deviation for this price feature
	mu = numpy.average(prices)
	sigma = numpy.std(prices)
	mu = "%.2f" % mu
	sigma = "%.2f" % sigma

	# apply the kalman filter to the time series
	filters = Filters(prices, mu, sigma)
	kalman = filters.kalmanfilter()

	template = 'datavis/kalman.html'

	context = {
		'symbol': symbol,
		'dates': dates,
		'prices': prices,
		'kalman': kalman,
		'mu': mu,
		'sigma': sigma,
	}

	return direct_to_template(request, template, context)
