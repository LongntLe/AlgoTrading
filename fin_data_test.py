#this is for researching financial data, irrelevant to the app
#source: pp 91 pyalgocourse book
import pandas as pd
import oanda
from sample_data import generate_sample_data

def retrieve_data(): #we will create a method to retrieve data
	pass


h5 = pd.HDFStore('data.h5','w') #Storing data into HDF5
%time = h5['data'] = data

print h5

h5 = pd.HDFStore('data.h5','r') #Storing into HDF5
%time data_copy = h5['data']

data_copy.info()

h5.close()

