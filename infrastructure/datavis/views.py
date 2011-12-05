# Simple view created here.
from django.template import RequestContext, loader
from datavis.models import Data
from datavis.bpnn import NN
from django.http import HttpResponse
from django.shortcuts import render_to_response

import matplotlib.finance as finance
import matplotlib.mlab as mlab
import numpy as np
import datetime
import time

def index(request):

	if request.method == "POST" and request.is_ajax:
		symbol = request.POST["symbol"]
		if symbol == '':
			symbol = 'AAPL'
#		date1=datetime.datetime.strptime(request.POST["from"],'%Y-%m-%d')
#		date2=datetime.datetime.strptime(request.POST["to"],'%Y-%m-%d')
	else:
		symbol = 'AAPL'
	
	start = datetime.date(2006, 11, 30)
	end = datetime.date(2011, 12, 2)
	answer = 0
	
	# Catch CSV
	fh = finance.fetch_historical_yahoo(symbol, start, end)

	# From CSV to REACARRAY
	r = mlab.csv2rec(fh); fh.close()
	# Order by Desc
	r.sort()

	dates = r.date
	prices = r.adj_close
	
	# convert to epoch time for highcharts
	dates = [(int(time.mktime(time.strptime(date.strftime("%Y-%m-%d"), "%Y-%m-%d"))) - time.timezone)*1000 for date in dates]	
	
	# find the moving average of this time series
	ma20 = moving_average(prices, 20, type='simple')
	macd = moving_average_convergence(prices)
	
	input = normalize(dates)
	output = normalize(prices)
	
	### machine learning code for neural nets
	# create a network with two input, two hidden, and one output nodes
	#n = NN(1, 2, 1)
	#data = createtrainingdata(input, output)	
	#n.train(data)
	#currentdate = datetime.datetime.now()
	#epochcurrentdate = (int(time.mktime(time.strptime(currentdate.strftime("%Y-%m-%d"), "%Y-%m-%d"))) - time.timezone)*1000
	#testepochcurrentdate = (2/(max(dates) - min(dates))) * epochcurrentdate - 1
	#answer = unscale(n.test([[[testepochcurrentdate]]]), prices)
	
	t = loader.get_template('datavis/index.html')

	c = RequestContext(request, {
		'answer': answer,
		'symbol': symbol,
		'dates': dates,
		'prices': prices,
		'ma20': ma20,
		'macd': macd,
	})

	return HttpResponse(t.render(c))

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

def moving_average(x, n, type='simple'):
	    x = np.asarray(x)
	    if type=='simple':
	        weights = np.ones(n)
	    else:
	        weights = np.exp(np.linspace(-1., 0., n))

	    weights /= weights.sum()

	    a =  np.convolve(x, weights, mode='full')[:len(x)]
	    a[:n] = a[n]
	    return a

def moving_average_convergence(x, nslow=26, nfast=12):
	    emaslow = moving_average(x, nslow, type='exponential')
	    emafast = moving_average(x, nfast, type='exponential')
	    return (emafast - emaslow)
	