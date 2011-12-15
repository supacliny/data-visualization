import math
import random
import string

random.seed(0)

# calculate a random integer:  a <= rand < b
def rand(a, b):
	return (b-a)*random.random() + a

# create matrix
def makeMatrix(I, J, fill=0.0):
	m = []
	for i in range(I):
		m.append([fill]*J)
	return m

# sigmoid function using tanh (standard sigmoid = 1/(1+e^-x))
def sigmoid(x):
	return math.tanh(x)

# derivative of the sigmoid function in terms of the output y
def dsigmoid(y):
	return 1.0 - y**2

class NeuralNet:
	"""
	A NeuralNet instantiation is used to predict the next-day price.
	Historical data is used to train the NN.

	Parameters
	----------
	ni: number of input nodes
	nh: number of hidden nodes
	no: number of output nodes

	Returns
	-------
	None
	"""
	def __init__(self, ni, nh, no):
		# number of input, hidden, and output nodes
		self.ni = ni + 1 # +1 for bias node
		self.nh = nh
		self.no = no

		# activations for nodes
		self.ai = [1.0]*self.ni
		self.ah = [1.0]*self.nh
		self.ao = [1.0]*self.no

		# create weights
		self.wi = makeMatrix(self.ni, self.nh)
		self.wo = makeMatrix(self.nh, self.no)
		# set them to random vaules
		for i in range(self.ni):
			for j in range(self.nh):
				self.wi[i][j] = rand(-0.2, 0.2)
		for j in range(self.nh):
			for k in range(self.no):
				self.wo[j][k] = rand(-2.0, 2.0)

		# last change in weights for momentum   
		self.ci = makeMatrix(self.ni, self.nh)
		self.co = makeMatrix(self.nh, self.no)


	def update(self, inputs):
		"""
		Update the weights associated with each node.

		Parameters
		----------
		inputs: updated values

		Returns
		-------
		ao: array of activations for that node
		"""
		if len(inputs) != self.ni-1:
			raise ValueError, 'wrong number of inputs'

		# input activations
		for i in range(self.ni-1):
			self.ai[i] = inputs[i]

		# hidden activations
		for j in range(self.nh):
			summ = 0.0
			for i in range(self.ni):
				summ = summ + self.ai[i] * self.wi[i][j]
			self.ah[j] = sigmoid(summ)

		# output activations
		for k in range(self.no):
			summ = 0.0
			for j in range(self.nh):
				summ = summ + self.ah[j] * self.wo[j][k]
				self.ao[k] = sigmoid(summ)

				return self.ao[:]


	def backPropagate(self, targets, N, M):
		"""
		Backpropagation algorithm using gradient decent.
		The algorithm first goes forward to get initial weights.
		Then it goes backward to update each activation with an error.
		Does these two steps for each input tuple.

		Parameters
		----------
		targets: y value of training (x,y)
		N: learning rate
		M: momentum factor

		Returns
		-------
		error: array of errors for each layer
		"""
		if len(targets) != self.no:
			raise ValueError, 'wrong number of target values'

		# calculate error terms for output
		output_deltas = [0.0] * self.no
		for k in range(self.no):
			error = targets[k]-self.ao[k]
			output_deltas[k] = dsigmoid(self.ao[k]) * error

		# calculate error terms for hidden
		hidden_deltas = [0.0] * self.nh
		for j in range(self.nh):
			error = 0.0
			for k in range(self.no):
				error = error + output_deltas[k]*self.wo[j][k]
				hidden_deltas[j] = dsigmoid(self.ah[j]) * error

		# update output weights
		for j in range(self.nh):
			for k in range(self.no):
				change = output_deltas[k]*self.ah[j]
				self.wo[j][k] = self.wo[j][k] + N*change + M*self.co[j][k]
				self.co[j][k] = change

		# update input weights
		for i in range(self.ni):
			for j in range(self.nh):
				change = hidden_deltas[j]*self.ai[i]
				self.wi[i][j] = self.wi[i][j] + N*change + M*self.ci[i][j]
				self.ci[i][j] = change

		# calculate error
		error = 0.0
		for k in range(len(targets)):
			error = error + 0.5*(targets[k]-self.ao[k])**2
		return error


	def test(self, patterns):
		"""
		Returns the next-day price after training with historical data.

		Parameters
		----------
		patterns: x value of training (x,y)

		Returns
		-------
		answer: the next day price!
		"""
		for p in patterns:
			answer = self.update(p[0])
		return answer[0]


	def train(self, patterns, iterations=1000, N=0.5, M=0.1):
		"""
		Train Neural net with historical prices for that stock.

		Parameters
		----------
		patterns: array of input data 
		iterations: number of iterations for gradient descent to minimize error
		N: learning rate
		M: momemtum factor

		Returns
		-------
		None
		"""
		for i in xrange(iterations):
			error = 0.0
			for p in patterns:
				inputs = p[0]
				targets = p[1]
				self.update(inputs)
				error = error + self.backPropagate(targets, N, M)
			if i % 100 == 0:
				pass #print 'error %-14f' % error
