from datavis.neuralnet import NeuralNet
import datetime
import time

class Predictors:
	"""this class will attempt to instantiate a prediction object"""


	def __init__(self, dates, prices):
		# list of dates and stock prices
		self.dates = dates
		self.prices = prices


	def predict(self):
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

		projection = self.unscale(neuralnetwork.test([[[self.normalize(tomorrow, self.dates)]]]), self.prices)

		return projection


	def normalize(self, value, listA):
		# we want to normalize the input and output data to a -1 to +1 range
		oldRange = max(listA) - min(listA)
		newRange = 2
		scale = (((value - min(listA)) * newRange) / float(oldRange)) - 1
		return scale


	def unscale(self, value, listA):
		# now we want to unscale the value
		oldRange = max(listA) - min(listA)
		newRange = 2
		answer = (((value + 1) * oldRange) / float(newRange)) + min(listA)
		return answer


	def create_training_data(self, listA, listB):
		# assemble the stock and prices as an array of arrays of arrays.
		pattern = []
		for index in range(len(listA)):
			pattern.append([[listA[index]], [listB[index]]])		
		return pattern

