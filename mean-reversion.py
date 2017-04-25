from event import OrderEvent
import pandas as pd
import numpy as np
from statisticaltest import hurst #calculating hurst exponent

'''
Strategy note:
To do:
	- How to take different ticks
		- calculate hurst as test first, can get historical data
	- How ADF tests
	-

'''

class meanrevertstrat(object):
	def __init__():
		self.instrument = instrument
        self.units = units
        self.events = events
        self.ticks = 0
        self.data = pd.DataFrame()

	def calculate(self, event):
		lookback = 20 # look back period length
		self.position = 0
		if event.type == "TICK":
            self.ticks += 1
		pass
