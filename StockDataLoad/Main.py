# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 20:22:28 2019

@author: Eric Bell
"""


#PullData is where we are getting the data; If It has insert in the name, it a SQL Transaction
from PullData.GetDataHistoric import HistoricalPricingInsert
from PullData.GetDataToday import TodayPricingInsert
from PullData.GetRobinhoodPrices import GetCurrentPrices


from UniverseData.universe import Faber_Ticker, SPY_Only_Universe

from db_loadfiles.connect_DB import BlueDream
from Analytics.trendy import  supres, gentrends, segtrends, minitrends, iterlines
from Analytics.LocalMaxMin import get_max_min, find_patterns,plot_minmax_patterns
#Build DataBase

#Universe = 
Universe = Faber_Ticker


HistoricalPricingInsert(Universe , '1h')
TodayPricingInsert(Universe)
GetCurrentPrices(Universe )


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
    max_min =get_max_min(df, smoothing, window)
    df.reset_index()['close'].plot()
    plt.scatter(max_min.index, max_min.values, color = 'orange', alpha = 0.50)
#    df.ema =df.close.ewm(com=0.5).mean()
#    df.head()
    ema=df.close.ewm(span=20,adjust=False).mean()
    patterns  =find_patterns(max_min)
    plot_minmax_patterns(df, max_min, patterns, stock, window, ema)

