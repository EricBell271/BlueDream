# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 20:22:28 2019

@author: Eric Bell
"""

##Add your connection to connect the DB.
from db_loadfiles.connect_DB import BlueDream


#PullData is where we are getting the data; If It has insert in the name, it a SQL Transaction
from PullData.GetDataHistoric import HistoricalPricingInsert
from PullData.GetDataToday import TodayPricingInsert

###This universe can be modified. I also have functions that can be added to add more stocks. 
from UniverseData.universe import Faber_Ticker, SPY_Only_Universe


#The Analytics folder is where all of the trend calculations are. 
from Analytics.trendy import  supres, gentrends, segtrends, minitrends, iterlines
from Analytics.LocalMaxMin import get_max_min, find_patterns,plot_minmax_patterns




#Universe = 
Universe = Faber_Ticker #Universe can be modified in the UniverseData.universe file. 


#Build DataBase
HistoricalPricingInsert(Universe , '1h') #This can be 1D to get daily date. 
#You do not have to run this everyday. This builds the historical data base for a year. This can be configured in 
#PullData.HistoricDataPullDates with the GetYearWindow function.
TodayPricingInsert(Universe) #This will insert the data in for the day.



from DBQuery.BlueDream import GetPrice


import pandas as pd

smoothing = 10
window =100
import matplotlib.pyplot as plt


for stock in Universe :
    historicData = GetPrice(BlueDream, stock)
#    print(historicData)
    df =pd.DataFrame(historicData, columns =['ticker', 'Date', 'Open','High',  'Low', 'close',  'volume', 'DateTime'])
    df.set_index(['ticker', 'DateTime' ])
    df.drop('Date', axis=1, inplace=True)
    df.head()
    max_min =get_max_min(df, smoothing, window)#this function calculates the min and max of the stocks. 
    df.reset_index()['close'].plot()##Run these two functions together
    plt.scatter(max_min.index, max_min.values, color = 'orange', alpha = 0.50)##to complete the plot
#    df.ema =df.close.ewm(com=0.5).mean()
#    df.head()
    ema=df.close.ewm(span=20,adjust=False).mean() ###Calculate the ema
    patterns  =find_patterns(max_min) ###Find stock patterns. 
    plot_minmax_patterns(df, max_min, patterns, stock, window, ema)

