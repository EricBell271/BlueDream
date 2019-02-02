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
from decimal import Decimal
#Universe = 
Universe = Faber_Ticker #Universe can be modified in the UniverseData.universe file. 


#Build DataBase
#data_status= HistoricalPricingInsert(Universe , '1h') #This can be 1D to get daily date. 
#print(data_status)
##You do not have to run this everyday. This builds the historical data base for a year. This can be configured in 
##PullData.HistoricDataPullDates with the GetYearWindow function.


todays_data_status=TodayPricingInsert(Universe, '1d') #This will insert the data in for the day.
print(todays_data_status)
def show():
    return(plt.show(block=True))


def is_num(value):
    try:
        value =Decimal(value)
        return True
    except:
        return False

smoothing = 10
window =25*8

def Signal(Universe):
    Signal_Status =[]
    for stock in Universe :
        historicData = GetPrice(BlueDream, stock)
#       print(historicData)

        df =pd.DataFrame(historicData, columns =['ticker', 'Date', 'Open','High',  'Low', 'close',  'volume', 'DateTime'])
        df.set_index(['ticker', 'DateTime' ])
        df['DateTime'] = pd.to_datetime(df['DateTime'])
        df['Date'] = pd.to_datetime(df['Date'])
        df['ema']=df.close.ewm(span=7*8,adjust=False).mean() ###Calculate the ema
        max_min =get_max_min(df, smoothing, window).rename('CriticalPoint')
        #this function calculates the min and max of the stocks. 
        todays_data= pd.concat([df , max_min], axis =1).tail(1)
        #    print(todays_data)
        todays_data.columns

        if (todays_data['ema'].values > todays_data['close'].values) and is_num(todays_data['CriticalPoint'].values):
            r='Bullish Signal'
        elif (todays_data['ema'].values < todays_data['close'].values) and is_num(todays_data['CriticalPoint'].values):
            r='Bearish Signal'
        else :
            r= 'No Signal' 
        Signal_Status.append([stock, r, str(todays_data['DateTime'].values[0])])
    return(Signal_Status)
Signal = Signal(Universe)

for i in range(len(Signal)):
    print(Signal[i])
#############pLotting 

#for stock in Universe :
#    historicData = GetPrice(BlueDream, stock)
##    print(historicData)
#    df =pd.DataFrame(historicData, columns =['ticker', 'Date', 'Open','High',  'Low', 'close',  'volume', 'DateTime'])
#    df.set_index(['ticker', 'DateTime' ])
#    df['DateTime'] = pd.to_datetime(df['DateTime'])
#    df['Date'] = pd.to_datetime(df['Date'])
#    df['ema']=df.close.ewm(span=7*8,adjust=False).mean() ###Calculate the ema
#    max_min =get_max_min(df, smoothing, window)#this function calculates the min and max of the stocks. 
#    
##    df1 =pd.DataFrame(max_min)
##    df1.reset_index()  
##    df.merge(df1, on= df.index)
##    df.drop('Date', axis=1, inplace=True)
#    df.head()
#
#    df.reset_index()['close'].plot()##Run these two functions together
#    df.reset_index()['ema'].plot()
#
#    df.reset_index()['close'].plot()##Run these two functions together
#    df.reset_index()['ema'].plot()
#    plt.scatter(max_min.index, max_min.values, color = 'orange', alpha = 0.50)##to complete the plotema=df.close.ewm(span=20,adjust=False).mean() ###Calculate the ema
#    show()
