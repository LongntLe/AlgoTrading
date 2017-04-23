from event import OrderEvent
import pandas as pd
import numpy as np

'''
Strategy note:
To do:
	- How to take different ticks
	- How ADF tests 

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

	def ADFtest():
		pass

	def hurst(context, data, sid):
    # Gathers all the prices that you need
    gather_prices(context, data, sid, 40) #need to fetch data somehow
    # Checks whether data exists
    data_gathered = gather_data(data)
    if data_gathered is None:
        return    
    
    tau, lagvec = [], []
    # Step through the different lags
    for lag in range(2,20):  
        # Produce price different with lag
        pp = numpy.subtract(context.past_prices[lag:],context.past_prices[:-lag])
        # Write the different lags into a vector
        lagvec.append(lag)
        # Calculate the variance of the difference
        tau.append(numpy.sqrt(numpy.std(pp)))
    # Linear fit to a double-log graph to get power
    m = numpy.polyfit(numpy.log10(lagvec),numpy.log10(tau),1)
    # Calculate hurst
    hurst = m[0]*2
    
    return hurst