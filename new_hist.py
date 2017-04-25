import pandas as pd

import datetime as dt
import v20

import configparser

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pylab

#new_hist.py

config = configparser.ConfigParser()
config.read('pyalgo.cfg')
access_token = config['oanda_v20']['access_token']

#v20.context
ctx = v20.Context(
	'api-fxpractice.oanda.com',
	443,
	True,
	application='sample_code',
	token = config['oanda_v20']['access_token'],
	datetime_format='RFC3339'
	)

response = ctx.account.instruments(config['oanda_v20']['account_id'])
r = response.get('instruments')

#dateTime formatting
suffix = '.000000000Z'
time1 = dt.datetime(2016,8,1,0,0,0)
d1 = time1.isoformat('T') + suffix
time2 = dt.datetime(2016,8,2,0,0,0)
d2 = time2.isoformat('T') + suffix
time_unit = dt.timedelta(1)
limit = dt.datetime(2016,8,15,0,0,0)
limit = limit.isoformat('T') + suffix

#data chunking
prices = pd.DataFrame()
dates = pd.date_range(start = d1, end = limit, freq = 'D')
for i in range(len(dates)-1):
	d1 = str(dates[i]).replace(' ', 'T')
	d2 = str(dates[i+1]).replace(' ', 'T')
	candle = ctx.instrument.candles(
		instrument = 'EUR_USD',
		fromTime = d1,
		toTime = d2,
		granularity = 'M1',
        price = 'A'
	)
	data = candle.get('candles')
	data = [cs.dict() for cs in data] #turn data into dict, pretty important
	for cs in data:
		cs.update(cs['ask'])
		del cs['ask']
	Kappa = pd.DataFrame(data)
	prices = prices.append(Kappa)

#translate the data into dictionary and pandas DataFrame

#create dataframe
#prices = pd.DataFrame(data)
print(prices)
prices["time"] = pd.to_datetime(prices["time"])
prices = prices.set_index("time")
prices.index = pd.DatetimeIndex(prices.index)
prices.to_hdf("data.h5", "data", format="table")

#Testing dataviz configuration
def visualization_facet(df):
	# Initialize a grid of plots with an Axes for each walk
	grid = sns.FacetGrid(df, col="walk", hue="walk", col_wrap=5, size=1.5)

	# Draw a horizontal line to show the starting point
	grid.map(plt.axhline, y=0, ls=":", c=".5")

	# Draw a line plot to show the trajectory of each random walk
	grid.map(plt.plot, "step", "position", marker="o", ms=4)

	# Adjust the tick positions and labels
	grid.set(xticks=np.arange(5), yticks=[-3, 3],
	         xlim=(-.5, 4.5), ylim=(-3.5, 3.5))

	# Adjust the arrangement of the plots
	grid.fig.tight_layout(w_pad=1)


def visualization_COLH(df):
	# We will visualize historical data using COLH format
	pass

def meanrevertstrat():
	pass

#vectorized backtest momentum strategy
"""
prices[["c", "l", "h", "o"]] = prices[["c", "l", "h", "o"]].astype("float64")
prices = prices.rename(columns={"c": "closeAsk", "l":"lowAsk",
                            "h": "highAsk", "o":"openAsk"})
prices[["closeAsk", "volume"]].head()

prices["returns"] = np.log(prices["closeAsk"] / prices["closeAsk"].shift(1))

cols = []

for momentum in [5, 15, 30, 60, 120]:
    col = "position_%s" % momentum
    prices[col] = np.sign(prices["returns"].rolling(momentum).mean())
    cols.append(col)

strats = ["returns"]

for col in cols:
    strat = "strategy_%s" % col.split("_")[1]
    prices[strat] = prices[col].shift(1) * prices["returns"]
    strats.append(strat)


prices[strats].dropna().cumsum().apply(np.exp).plot()
plt.grid()
plt.show()
"""
