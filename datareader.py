# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 15:10:07 2018

@author: root
"""

import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import pandas_datareader.data as web
from pandas_datareader import data,wb
import requests
import time


def get_stock_info(stock, start, end, source='morningstar'):
    df = data.DataReader(stock, source, start, end)
    df['Stock'] = stock
    agg = df.groupby('Stock').agg({
        'Open': ['min', 'max', 'mean', 'median'],
        'Close': ['min', 'max', 'mean', 'median'],
        'High': ['min', 'max', 'mean', 'median'],
        'Low': ['min', 'max', 'mean', 'median'],
    })
    agg.columns = [' '.join(col).strip() for col in agg.columns.values]
    return agg.to_json()
   
   
def datetime_timestamp(dt):
     time.strptime(dt, '%Y-%m-%d %H:%M:%S')
     s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
     return str(int(s))

   
   
def get_from_yahoo():
	s = requests.Session()
	
	#Replace B=xxxx
	cookies = dict(B='c650m5hchrhii&b=3&s=tk')
	
	#Replace crumb=yyyy
	crumb = 'NMhMTCv7QpM'
	
	begin = datetime_timestamp("2014-01-01 09:00:00")
	    
	end = datetime_timestamp("2017-04-30 09:00:00")
	
	r = s.get("https://query1.finance.yahoo.com/v7/finance/download/IBM?period1="+begin+"&period2="+end+"&interval=1d&events=history&crumb="+crumb,cookies=cookies,verify=False)
	   
	f = open('IBM.csv', 'w')
	f.write(r.text)
	f.close()
	es = pd.read_csv('IBM.csv', index_col=0,parse_dates=True, sep=",", dayfirst=True)
	    
	data = pd.DataFrame({"IBM" : es["Adj Close"][:]}) 
	    
	print(data.info())
	    
	data.plot(subplots=True, grid=True, style="b", figsize=(8, 6))
	    
	plt.show()


if __name__=='__main__':
	year=[1950,1970,1990,2010]
	pop=[2.519,3.692,5.263,6.972]
	#plt.plot(year,pop)
	#plt.show()
	
	start = datetime.datetime(2017, 1, 1) # or start = '1/1/2016'
	end = datetime.date.today()
	#print(get_stock_info('AAPL',start,end))
	#print(get_stock_info('JD',start,end))
	#prices = web.DataReader('AAPL', 'morningstar', start, end)
	JD = web.DataReader('JD', data_source='morningstar',start='1/1/2017',end='1/1/2018')
	print(JD.sample(5))
	#print(JD.info())
	#JD['Log_Ret'] = np.log(JD['Close']/JD['Close'].shift(1))
	#JD['volatility'] = pd.rolling_std(JD['Log_Ret'],window=252) * np.sqrt(252)
	#plt.inline(JD[['Close','Volatility']].plot(subplots=True,color='blue',figsize=(8,6))
	
	JD['Close'].plot(figsize=(8,5))
	

	#web.get_data_yahoo('600624.ss','7/1/2015','8/20/2015')	
	#get_from_yahoo()
	#print("Hello python")