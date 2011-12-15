from datavis.neuralnet import NeuralNet
import datetime
import time

class Predictors:
	"""
	A Predictor instantiation is used as an api to predictor classes like Neural Net.
	Ultimately, we want to have several types of predictors like SVMs, Bayesians, HMMs.

	Parameters
	----------
	dates: historical dates of a particular stock
	prices: historical prices of same stock

	Returns
	-------
	None
	"""
	def __init__(self, dates, prices):
		# list of dates and stock prices
		self.dates = dates
		self.prices = prices


	def predict(self):
		"""
		Trigger a prediction event for the next day after normalizing input data.

		Parameters
		----------
		None

		Returns
		-------
		projection: the projected next day price for that stock.
		"""
		# normalize the input and ouput data and the combine
		inputdata = [self.normalize(elem, self.dates) for elem in self.dates]
		outputdata = [self.normalize(elem, self.prices) for elem in self.prices]
		combinedata = self.create_training_data(inputdata, outputdata)

		# create a network with 1 input, 2 hidden, 1 output nodes, then train
		neuralnetwork = NeuralNet(1, 2, 1)
		neuralnetwork.train(combinedata)

		# get the date of tomorrow to predict that date
		tomorrow = datetime.date.today() + datetime.timedelta(days=1)
		tomorrow = (int(time.mktime(time.strptime(tomorrow.strftime("%Y-%m-%d"), "%Y-%m-%d"))) - time.timezone)*1000

		# magic of math!
		projection = self.unscale(neuralnetwork.test([[[self.normalize(tomorrow, self.dates)]]]), self.prices)

		return projection


	def normalize(self, value, listA):
		"""
		Normalize the input data in the range -1 to +1 for better NN performance.

		Parameters
		----------
		value: value of the input to be scaled
		listA: use this list to scale that value

		Returns
		-------
		scale: the scaled value of the input
		"""
		oldRange = max(listA) - min(listA)
		newRange = 2
		scale = (((value - min(listA)) * newRange) / float(oldRange)) - 1
		return scale


	def unscale(self, value, listA):
		"""
		Unscale the value to get the original answer.

		Parameters
		----------
		value: value of the input to be unscaled
		listA: use this list to unscale that value

		Returns
		-------
		answer: the unscaled projected value in the range of listA
		"""
		oldRange = max(listA) - min(listA)
		newRange = 2
		answer = (((value + 1) * oldRange) / float(newRange)) + min(listA)
		return answer


	def create_training_data(self, listA, listB):
		"""
		Assemble the dates and prices as an array of arrays of arrays for highcharts.

		Parameters
		----------
		listA: pattern[0][0]
		listB: pattern[0][1]

		Returns
		-------
		pattern: an array of 2 arrays
		"""
		pattern = []
		for index in range(len(listA)):
			pattern.append([[listA[index]], [listB[index]]])		
		return pattern

