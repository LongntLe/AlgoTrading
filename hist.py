"""Download historical data from oanda using oandaAPI V2.0 
    import downloaded data into .txt file
    automate downloading"""

import os

import bs4
import requests

import json 
import pandas as pd
from pandas.io.json import json_normalize

import time
from datetime import datetime
from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments

#API Setup
access_token = os.environ["OANDA_API_ACCESS_TOKEN"]
client = API(access_token=access_token)

def parse_instrument_list():
    #TODO:created_at record
    response = requests.get("https://www.oanda.com/forex-trading/markets/live")
    soup = bs4.BeautifulSoup(response.text)
    txt = soup.find('input', type="hidden")
    #TODO: make pairs scalable for all commodities
    pairs = txt["value"].split(", ")
    pairs = [pair.replace("/", "_") for pair in pairs]
    return pairs    

def download(instrument, params):
    r = instruments.InstrumentsCandles(instrument=instrument, params=params)
    client.request(r)
    data = r.response
    df = json_normalize(data["candles"])
    df["granularity"] = (data["granularity"])
    df["instrument"] = data["instrument"]
    return df

if __name__ == "__main__":
    instrument = parse_instrument_list()
    #TODO: Download data in chunk
    d1 = "2016-01-01"
    d1 = time.mktime(time.strptime(d1, '%Y-%m-%d'))
    d2 = "2017-01-01"
    d2 = time.mktime(time.strptime(d2, '%Y-%m-%d'))
    #daterange = pd.date_range(d1, d2, freq = 'D')
    df = pd.DataFrame()
    #for i in range(0, len(daterange)):
    #    d1 = daterange[i]
    #    d2 = daterange[i+1]
    params = {"granularity":'H12', "from":d1, "to":d2}
    for pair in instrument:
        try:
            data = download(pair, params)
            df = df.append(pd.DataFrame(data))
        except:
            print("ERROR") #TODO: classify errors
            pass
    df.to_csv(r'data.txt', header=None, index=None, sep=' ', mode='a')
    print("Successfully add data to data.txt as csv")
