# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 19:49:36 2019

@author: Eric Bell
"""

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
from PullData.GetTwitterData import InsertHashtagData
from PullData.GetStockTickerMJ import LegalizeIt

###This universe can be modified. I also have functions that can be added to add more stocks. 
from UniverseData.universe import Faber_Ticker, SPY_Only_Universe


#The Analytics folder is where all of the trend calculations are. 
from Analytics.trendy import  supres, gentrends, segtrends, minitrends, iterlines
from Analytics.LocalMaxMin import get_max_min, find_patterns,plot_minmax_patterns




#Universe = 
Universe = Faber_Ticker #Universe can be modified in the UniverseData.universe file. 
#LegalizeIt()

#Build DataBase
#HistoricalPricingInsert(Universe , '1h') #This can be 1D to get daily date. 
#You do not have to run this everyday. This builds the historical data base for a year. This can be configured in 
#PullData.HistoricDataPullDates with the GetYearWindow function.
#TodayPricingInsert(Universe) #This will insert the data in for the day.
#InsertHashtagData(Universe) 


from DBQuery.BlueDream import GetPrice


import pandas as pd

import matplotlib.pyplot as plt
from math import isnan
from decimal import Decimal
def is_num(value):
    try:
        value =Decimal(value)
        return True
    except:
        return False

        

def GetLocalCriteria(Universe, smooth_Length, window_Length, charts = True) :
#    Signal_Status = []
    SignalReturn= []
    smoothing = smooth_Length
    window = window_Length
    for stock in Universe :
        print(stock)
        historicData = GetPrice(BlueDream, stock)
        #    print(historicData)
        df =pd.DataFrame(historicData, columns =['ticker', 'Date', 'Open','High',  'Low', 'close',  'volume', 'DateTime'])
        df.set_index(['ticker', 'DateTime' ])
        df.drop('Date', axis=1, inplace=True)
        df['ema']=df.close.ewm(span=20,adjust=False).mean() #
        max_min =get_max_min(df, smoothing, window)#this function calculates the min and max of the stocks. 
        #this function calculates the min and max of the stocks. 
        Signal_data= pd.concat([df , max_min], axis =1)
        
        Signal_data.columns
        #this function calculates the min and max of the stocks. 
        Signal_data= pd.concat([df , max_min], axis =1)
        Signal_data= pd.concat([df , max_min.rename('CriticalPoint')], axis =1)
        #    print(todays_data)
        Signal_data.columns
        Signal_data['Signal'] = 0
        Signal_data.loc[Signal_data['ema'] >=  Signal_data['CriticalPoint'], 'Signal'] = 1
        Signal_data.loc[Signal_data['ema'] <=  Signal_data['CriticalPoint'], 'Signal'] = -1
        SignalReturn.append(Signal_data)
        if charts == True: 

            df.reset_index()['close'].plot()##Run these two functions together
            df.ema.plot()
            
            plt.scatter(max_min.index, max_min.values, color = 'orange', alpha = 0.50)##to complete the plot
            plt.show()
    return(SignalReturn)
    
data  = GetLocalCriteria(Universe, smooth_Length= 20, window_Length =25 , charts = False)
