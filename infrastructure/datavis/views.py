from django.template import RequestContext, loader
from datavis.models import Data
from datavis.neuralnet import NeuralNet
from datavis.indicators import Indicators
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
		symbol = 'AAPL'
	
	start = datetime.date(2006, 01, 01)
	end = datetime.datetime.now()

	### machine learning code for neural nets
	#projection= 0
	#input = normalize(dates)
	#output = normalize(prices)	
	# create a network with two input, two hidden, and one output nodes
	#n = NN(1, 2, 1)
	#data = createtrainingdata(input, output)	
	#n.train(data)
	#currentdate = datetime.datetime.now()
	#epochcurrentdate = (int(time.mktime(time.strptime(currentdate.strftime("%Y-%m-%d"), "%Y-%m-%d"))) - time.timezone)*1000
	#testepochcurrentdate = (2/(max(dates) - min(dates))) * epochcurrentdate - 1
	#answer = unscale(n.test([[[testepochcurrentdate]]]), prices)
	
	dates, prices = get_stock_history(symbol, start, end)

	# find the MA and MACD of this time series
	indicators = Indicators(prices)	
	ma20 = indicators.moving_average(20, type='simple')
	macd = indicators.moving_average_convergence()
	
	template = 'datavis/index.html'

	context = {
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

	
def unscale(value, list):
		answer = (value + 1) / (2/max(list) - min(list))
		return answer

def createtrainingdata(listA, listB):
	pattern = []
	for index in range(len(listA)):
		pattern.append([[listA[index]], [listB[index]]])
		
	return pattern

def normalize(list):
	precompute = 2/(max(list) - min(list))
	scale = [precompute * elem - 1 for elem in list]
	return scale


	