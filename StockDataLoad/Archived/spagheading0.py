#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 19:57:44 2019

@author: ebell
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 20:22:28 2019

@author: Eric Bell
"""
import matplotlib.pyplot as plt
from DBQuery.BlueDream import GetPrice
import pandas as pd

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
#data_status= HistoricalPricingInsert(Universe , '1d') #This can be 1D to get daily date. 
#print(data_status)
##You do not have to run this everyday. This builds the historical data base for a year. This can be configured in 
##PullData.HistoricDataPullDates with the GetYearWindow function.
#todays_data_status=TodayPricingInsert(Universe) #This will insert the data in for the day.
#print(todays_data_status)
def show():
    return(plt.show(block=True))

#def CreateDF(Universe ):
#    for stock in Universe :
#    historicData = GetPrice(BlueDream, stock)
##    print(historicData)
#    df =pd.DataFrame(historicData, columns =['ticker', 'Date', 'Open','High',  'Low', 'close',  'volume', 'DateTime'])
#    df.set_index(['ticker', 'DateTime' ])
##    df.drop('Date', axis=1, inplace=True)
smoothing = 10
window =25


for stock in Universe :
    historicData = GetPrice(BlueDream, stock)
#    print(historicData)
    df =pd.DataFrame(historicData, columns =['ticker', 'Date', 'Open','High',  'Low', 'close',  'volume', 'DateTime'])
    df.set_index(['ticker', 'DateTime' ])
#    df.drop('Date', axis=1, inplace=True)
    df.head()
    df['ema']=df.close.ewm(span=20,adjust=False).mean() ###Calculate the ema
    max_min =get_max_min(df, smoothing, window)#this function calculates the min and max of the stocks. 
    print(max_min)
    
    df.plot('close', 'Date')##Run these two functions together
    plt.scatter(max_min.index, max_min.values, color = 'orange', alpha = 0.50)##to complete the plotema=df.close.ewm(span=20,adjust=False).mean() ###Calculate the ema
    
    show()

