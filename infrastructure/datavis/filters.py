import numpy
import math


class Filters:
	"""
	A Filters instantiation is an object containing a Kalman Filter.

	Parameters
	----------
	prices: array of historical stock prices
	mu: average of these prices
	sigma: standard deviation of these prices

	Returns
	-------
	None
	"""
	def __init__(self, prices, mu, sigma):
		self.prices = prices
		self.mu = mu
		self.sigma = sigma


	def kalmanfilter(self):
		"""
		The Kalman filter is a mathematical method used to use measure observations over time, 
		containing noise (random variations) and other inaccuracies, 
		and produce values that tend to be closer to the true values of the measurements.

		This is a code implementation of the algorithm given in pages 11-15 of An Introduction to the Kalman Filter 
		by Greg Welch and Gary Bishop, University of North Carolina at Chapel Hill, Department of Computer Science.

		Parameters
		----------
		None

		Returns
		-------
		xhat: array of dynamically predicted prices given actual prices
		"""
		# intial parameters
		iterations = len(self.prices)
		# size of array
		size = (iterations,)
		# truth value which is the average of actual prices
		x = self.mu
		# actual prices
		z = self.prices

		# process variance
		Q = 1e-5

		# allocate space for arrays
		xhat = numpy.zeros(size)      # a posteri estimate of x
		P = numpy.zeros(size)         # a posteri error estimate
		xhatminus = numpy.zeros(size) # a priori estimate of x
		Pminus = numpy.zeros(size)    # a priori error estimate
		K = numpy.zeros(size)         # gain or blending factor

		# estimate of measurement variance
		R = 0.1**2 

		# intial estimates
		xhat[0] = z[0]
		P[0] = 1.0

		# the algorithm consists of two parts: predict and correct
		for k in range(1,iterations):
		    # predict (time update)
		    xhatminus[k] = xhat[k-1]
		    Pminus[k] = P[k-1]+Q

		    # correct (measurement update)
		    K[k] = Pminus[k]/( Pminus[k]+R )
		    xhat[k] = xhatminus[k]+K[k]*(z[k]-xhatminus[k])
		    P[k] = (1-K[k])*Pminus[k]

		return xhat
