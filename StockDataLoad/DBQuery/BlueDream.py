# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 19:11:10 2018

@author: Eric Bell
"""


    
from db_loadfiles.connect_DB import BlueDream

def GetPrice(Database, ticker):
    DB = Database
    cursor = DB.cursor()
    cursor.execute("""select *
                   --a.DateTime,a.Open,a.High,  a.Low, a.close,  a.volume
                    from tickerdateprice a
                   where a.ticker ='%s' 
                   """  % ticker)
    PricingData= cursor.fetchall()
    return(PricingData)

#GetPrice(BlueDream, 'AGG')

def GetPriceSpecifyDate(Database, ticker, date):
    ticker ='AGG'
    Date ='2019-01-23'
    DB = Database
    cursor = DB.cursor()
    cursor.execute("""select *
                    from tickerdateprice a
                   where a.ticker ='%s'
                   and a.Date >'%s' 
                   """  % (ticker, Date))
    PricingData= cursor.fetchall()
    return(PricingData)
#GetPriceSpecifyDate(BlueDream, 'AGG', '2019-01-23')

##    
##len(GetPrice(Database =  BlueDream))
#GetPrice(Database =  BlueDream)
##len(GetSentimentPriceDateNegative(BlueDream))
#def GetTickerNames(Database):
#    
#    DB = Database
#    cursor = DB.cursor()
#    cursor.execute("""select distinct a.Ticker, a.price
#               from TickerName a
#               where cast(a.price as float) > 5 
#               """)
#    MMJ_Ticker= cursor.fetchall()
#    return(MMJ_Ticker)
##GetTickerNames(BlueDream)
#    
#    
#def GetCompanyNames(Database):
#    
#    DB = Database
#    cursor = DB.cursor()
#    cursor.execute("""select distinct CompanyName, a.mktcap
#               from TickerName a
#                """)
#    MMJ_Ticker= cursor.fetchall()
#    return(MMJ_Ticker)
#
##MMJ_Ticker = GetCompanyNames(BlueDream)
#    
#def GetSupRes(Database):
#    
#    DB = Database
#    cursor = DB.cursor()
#    cursor.execute("""select *
#                    from tickerdatesupportresistance a
#
#                   ;""")
#    PricingData= cursor.fetchall()
#    return(PricingData)
##    
#    
#GetSupRes(BlueDream)
