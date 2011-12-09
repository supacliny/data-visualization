from scipy import *
from scipy import fftpack

class FFT:
	"""this class defines a fast fourier transform algorithm that can identify patterns."""

	def __init__(self, prices dates):
		# list of stock prices
		self.prices = prices
		self.dates = dates

		
	def fft(self):

		transform = fft(prices)

		transformsize = len(transform)

		power = abs(transform[1:(transformsize/2)])**2

		nyquist = 1./2

		frequency = array(range(transformsize/2))/(transformsize/2.0)*nyquist

		period = 1./frequency
		
		return period[1:len(period)], power
