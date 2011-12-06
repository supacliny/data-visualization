from django.template import RequestContext, loader
from datavis.models import Data
from datavis.indicators import Indicators
from datavis.predictors import Predictors
from django.http import HttpResponse
from django.views.generic.simple import direct_to_template

import matplotlib.finance as finance
import matplotlib.mlab as mlab
import numpy as np
import datetime
import time


def index(request):
	"""this function handles churning out the data for the context specific to index.html"""
	
	if request.method == "POST" and request.is_ajax():
		symbol = request.POST.get("symbol")
	else:
		symbol = 'EBAY'
	
	start = datetime.date(2006, 01, 01)
	end = datetime.datetime.now()	
	dates, prices = get_stock_history(symbol, start, end)

	# find the MA and MACD of this time series
	indicators = Indicators(prices)	
	ma20 = indicators.moving_average(20, type='simple')
	macd = indicators.moving_average_convergence()
	
	# find the next day stock price in this time series
	predictor = Predictors(dates, prices)
	projection = predictor.predict()

	template = 'datavis/index.html'

	context = {
		'projection': projection,
		'symbol': symbol,
		'dates': dates,
		'prices': prices,
		'ma20': ma20,
		'macd': macd,
	}

	return direct_to_template(request, template, context)


def get_stock_history(symbol, start, end):
	"""given a stock symbol as a string, produces a dictionary of historical data"""

	stock_history = finance.fetch_historical_yahoo(symbol, start, end)
	r = mlab.csv2rec(stock_history)
	r.sort()

	dates = r.date
	prices = r.adj_close
	
	#convert to epoch time for highcharts
	dates = [(int(time.mktime(time.strptime(date.strftime("%Y-%m-%d"), "%Y-%m-%d"))) - time.timezone)*1000 for date in dates]
	
	return dates, prices

	


	