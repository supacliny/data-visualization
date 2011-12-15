from scipy import *
from scipy import fftpack

class Transforms:
	"""this class defines a fast fourier transform algorithm that can identify patterns."""

	def __init__(self, prices):
		# list of stock prices
		self.prices = prices
		
	def fft2(self):

		transform = fft(self.prices)

		transformsize = len(transform)

		power = abs(transform[1:(transformsize/2)])**2

		nyquist = 1./2

		frequency = array(range(transformsize/2))/(transformsize/2.0)*nyquist

		frequency = frequency[1:len(frequency)]

		period = 1./frequency
		
		return period, power
