import numpy
import math

class Filters:
	"""this class generates a Kalman Filter"""

	def __init__(self, prices, mu, sigma):
		# list of stock prices
		self.prices = prices
		self.mu = mu
		self.sigma = sigma

	
	def kalmanfilter(self):
		
		# intial parameters
		n_iter = len(self.prices)
		sz = (n_iter,) # size of array
		x = self.mu # truth value 
		z = self.prices
		
		Q = 1e-5 # process variance

		# allocate space for arrays
		xhat = numpy.zeros(sz)      # a posteri estimate of x
		P = numpy.zeros(sz)         # a posteri error estimate
		xhatminus = numpy.zeros(sz) # a priori estimate of x
		Pminus = numpy.zeros(sz)    # a priori error estimate
		K = numpy.zeros(sz)         # gain or blending factor

		R = 0.1**2 # estimate of measurement variance, change to see effect

		# intial guesses
		xhat[0] = z[0]
		P[0] = 1.0

		for k in range(1,n_iter):
		    # time update
		    xhatminus[k] = xhat[k-1]
		    Pminus[k] = P[k-1]+Q

		    # measurement update
		    K[k] = Pminus[k]/( Pminus[k]+R )
		    xhat[k] = xhatminus[k]+K[k]*(z[k]-xhatminus[k])
		    P[k] = (1-K[k])*Pminus[k]

		return xhat
