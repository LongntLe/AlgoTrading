import pandas as pd

import datetime as dt
import v20

import configparser

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
d1 = dt.datetime(2016,8,1,0,0,0)
d1 = d1.isoformat('T') + suffix

d2 = dt.datetime(2016,8,2,0,0,0)
d2 = d2.isoformat('T') + suffix

candle = ctx.instrument.candles(
		instrument = 'EUR_USD',
		fromTime = d1,
		toTime = d2,
		granularity = 'S5'
	)

#translate the data into pandas DataFrame
data = candle.get('candles')
data = [cs.dict() for cs in data]
'''for cs in data:
	cs.update(cs['ask'])
	del cs['ask']'''

df = pd.DataFrame(data)
print(df)

