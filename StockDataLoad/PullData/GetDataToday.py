# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 21:55:28 2018

@author: Eric Bell
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 15:46:40 2018

@author: Eric Bell
"""

##Libraries--------------------------
import requests
import datetime
import time
import json
from db_loadfiles.connect_DB import BlueDream
from datetime import datetime as dt
#from DataBaseQuery import GetTickerNames
#from GetStockTickerMJ import LegalizeIt

#Retrieve pricing data

from PullData.GetDataHistoric import GetHistoricalPricing
#Universe = GetTickerNames(BlueDream)
#Universe = SPY_Only_Universe

def TodayPricingInsert(Universe):
    
    
    HistoricPricingData =[]
    for ticker in Universe:

        print(ticker)
#        today_date = dt.today().strftime('%Y-%m-%d')
        today_date = (dt.today().now() + datetime.timedelta(days=1, hours=0)).strftime('%Y-%m-%d')
        previous_date = (dt.today().now()).strftime('%Y-%m-%d')
        PricingData = GetHistoricalPricing(stock_abbr = ticker, 
                                    start_date = previous_date , 
                                    end_date = today_date , 
                                    interval = '1d')
        #print(PricingData)
        if PricingData != 'NO DATA' :
            for i in range(len(PricingData)):
                
                DateTime  = PricingData[i][0]
                Date = DateTime[:10]
                close    =PricingData[i][1]
                volume    =PricingData[i][2]
                high =  PricingData[i][3]
                low  = PricingData[i][4]
                Open= PricingData[i][5]
                HistoricPricingData.append([ticker, Date, Open, close, high, low, volume , DateTime])
                
    DB = BlueDream
    cursor = DB.cursor()

    try:
        cursor.executemany("INSERT INTO TickerDatePrice VALUES(%s,%s,%s,%s, %s, %s,%s, %s)", HistoricPricingData)    
        DB.commit()
        return('Data has been Pulled Today')
    except :
        return('Maybe Trade a Box Spread Today; Data Failed')




