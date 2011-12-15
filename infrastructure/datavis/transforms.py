import scipy as sci


class Transforms:
	"""
	A Transforms instantiation is an object with a Fast Fourier Transform function.

	Parameters
	----------
	prices: array of historical prices for a particular stock

	Returns
	-------
	None
	"""
	def __init__(self, prices):
		self.prices = prices


	def fft2(self):
		"""
		The Fast Fourier Transform algorithm transforms time-series data to the frequency domain.
		This means that periodic patterns show up as spikes on the graph.
		The Nyquist frequency is equal to half the maximum frequency -
		frequencies above the Nyquist frequency correspond to negative frequencies.

		Parameters
		----------
		None

		Returns
		-------
		period: array of periods for that input price
		power: the fft**2 value
		"""
		transform = sci.fft(self.prices)
		transformsize = len(transform)
		power = abs(transform[1:(transformsize/2)])**2
		nyquist = 1./2
		frequency = sci.array(range(transformsize/2))/(transformsize/2.0)*nyquist
		frequency = frequency[1:len(frequency)]
		period = 1./frequency

		return period, power
