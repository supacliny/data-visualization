# Simple view created here.
from django.template import RequestContext, loader
from datavis.models import Data
from django.http import HttpResponse
from django.shortcuts import render_to_response

from pylab import figure, show
from matplotlib.finance import quotes_historical_yahoo
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter
import datetime

def index(request):

	if request.method == "POST" and request.is_ajax:
		symbol = request.POST["symbol"]
		date1=datetime.datetime.strptime(request.POST["from"],'%Y-%m-%d')
		date2=datetime.datetime.strptime(request.POST["to"],'%Y-%m-%d')
	else:
		symbol = 'TXN'
		date1 = datetime.date(2011, 10, 6)
		date2 = datetime.date(2011, 11, 11)
	
	quotes = quotes_historical_yahoo(symbol, date1, date2)
	if len(quotes) == 0:
	    raise SystemExit

	dates = [q[0] for q in quotes]
	opens = [q[3] for q in quotes]

	dates = [(datetime.datetime.fromordinal(int(elem))).strftime("%Y-%m-%d") for elem in dates]
	opens = ["%.2f" % v for v in opens]
		
	t = loader.get_template('datavis/index.html')

	c = RequestContext(request, {
		'dates': dates,
		'opens': opens,
	})

	return HttpResponse(t.render(c))
	