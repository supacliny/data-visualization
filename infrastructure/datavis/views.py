from django.template import RequestContext, loader
from datavis.models import Data
from datavis.stocks import Stocks
from datavis.indicators import Indicators
from datavis.predictors import Predictors
from django.http import HttpResponse
from django.views.generic.simple import direct_to_template
import datetime
import time

def index(request):
	"""this function churns out the data for the context specific to index.html"""
	
	symbol = ""
	
	if request.method == "POST":
		symbol = request.POST.get("symbol")

	if symbol == "":
		symbol = 'EBAY'
		
	start = datetime.date(2006, 01, 01)
	end = datetime.datetime.now()

	# get the stock history for that symbol with start and end dates
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
	
	# find the next day stock price in this time series
	start = datetime.date(2006, 01, 01)
	end = datetime.datetime.now()
	
	# get the stock history for that symbol with start and end dates
	stock = Stocks(symbol, start, end)
	dates, prices = stock.get_stock_history()
	
	predictor = Predictors(dates, prices)
	projection = predictor.predict()
	projection = "%.2f" % projection
	
	#time.sleep(3)

	return HttpResponse(projection, mimetype="text/html")
	

def fft(request, symbol):
		
	# get the stock history for that symbol with start and end dates
	start = datetime.date(2006, 01, 01)
	end = datetime.datetime.now()
	stock = Stocks(symbol, start, end)
	dates, prices = stock.get_stock_history()
	
	template = 'datavis/fft.html'

	context = {
		'symbol': symbol,
		'dates': dates,
		'prices': prices,
	}

	return direct_to_template(request, template, context)
