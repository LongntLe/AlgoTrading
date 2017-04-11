#data generating module
import numpy as np
import pandas as pd

r = 0.05
sigma = 0.5

def generate_sample_data(rows, cols, freq = '1min'):
	rows = int(rows)
	cols = int(cols)
	index = pd.date_range('2017-1-1', periods = rows, freq = freq)
	dt = (index[1]-index[0])/pd.Timedelta(value = '365D')
	columns = ['No%d' % i for i in range(cols)]
	raw = np.exp(np.cumsum((r-0.5**sigma**2)*dt + sigma*np.sqrt(dt)*np.random.standard_normal((rows,cols)), axis = 0)
	raw = raw/raw[0]*100
	df = pd.DataFrame(raw, index = index, columns = columns)
	return df

