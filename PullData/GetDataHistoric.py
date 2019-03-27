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

from datetime import datetime as dt, timedelta
from DBQuery.BlueDream import  GetPrice
#from GetStockTickerMJ import LegalizeIt

#Retrieve pricing data
from PullData.HistoricDataPullDates import GetTodaysDate,  GetYearWindow




def GetHistoricalPricing(stock_abbr, start_date, end_date, interval) : 
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    url = 'https://query1.finance.yahoo.com/v8/finance/chart/' + stock_abbr + '?period1=' + str(int(time.mktime(start_date.timetuple()))) + '&period2=' + str(int(time.mktime(end_date.timetuple()))) + '&interval=' + interval + '&events=history&crumb=pa16aIx60zo'
    response = requests.get(url).content
#    print(url)
    try:
        temp_json = json.loads(response)
        temp_close = temp_json['chart']['result'][0]['indicators']['quote'][0]['close']
        temp_open = temp_json['chart']['result'][0]['indicators']['quote'][0]['open']
        temp_high = temp_json['chart']['result'][0]['indicators']['quote'][0]['high']
        temp_low = temp_json['chart']['result'][0]['indicators']['quote'][0]['low']
        temp_volume = temp_json['chart']['result'][0]['indicators']['quote'][0]['volume']
        temp_dates = [str(datetime.datetime.fromtimestamp(x)) for x in temp_json['chart']['result'][0]['timestamp']]
#        print(temp_high)
        return([[i, j, k, y , z, q] for i, j, k, y, z, q in zip(temp_dates, temp_close,  temp_volume,temp_high, temp_low, temp_open )])
    except:
        return('NO DATA')



#
#PricingData = GetHistoricalPricing(stock_abbr ='CGC', start_date = '2018-11-13',  end_date = '2018-11-14',   interval = '5m')
def HistoricalPricingInsert(Universe, time_interval):
    last_date = GetTodaysDate()
    start_date   = GetYearWindow()
    HistoricPricingData =[]
    for ticker in Universe:


        PricingData = GetHistoricalPricing(stock_abbr = ticker, start_date = str(start_date),  end_date =  str(last_date),   interval =time_interval )

        if PricingData != 'NO DATA' :
            for i in range(len(PricingData)):
#                print(i)
#                print(ticker)
                
                DateTime  = PricingData[i][0]
                Date = DateTime[:10]
                close    =PricingData[i][1]
                high =  PricingData[i][3]
                low  = PricingData[i][4]

                Open= PricingData[i][5]
                volume    =PricingData[i][2]
                HistoricPricingData.append([ticker, Date, Open, close, high, low, volume , DateTime])
                
    DB = BlueDream
    cursor = DB.cursor()
    table_name = "TickerDatePrice"
    cursor.execute("DROP TABLE IF EXISTS " + table_name)
    cursor.execute("""
                   CREATE TABLE {} (
                   

           Ticker VARCHAR(10),
           Date VARCHAR(20),
           Close REAL,
           Open Real,
           High REAL,
           Low REAL,
           Volume REAL, 
           DateTime VARCHAR(20)
           
	);   
    """.format(table_name))        
                
    try :            
        cursor.executemany("INSERT INTO TickerDatePrice VALUES(%s,%s,%s,%s, %s, %s, %s, %s)", HistoricPricingData)    
        DB.commit()
        return('Historical Data has been Pulled')
    except :
        return('Buy an Index Fund ;Historical Data Failure')
#
#from UniverseData.universe import Faber_Ticker, SPY_Only_Universe
#
#
#
#HistoricalPricingInsert(SPY_Only_Universe)