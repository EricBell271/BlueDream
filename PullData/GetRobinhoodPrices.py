# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 20:35:07 2019

@author: Eric Bell
"""
from Robinhood.connect_broker import my_trader
from UniverseData.universe import Faber_Ticker, SPY_Only_Universe
def GetCurrentPrices(Universe):
    TodayStockData = []
    for ticker in Universe:
        print(ticker)
        HarryHoodData =my_trader.quote_data(ticker)
        symbol = HarryHoodData['symbol']
        ask_price = HarryHoodData['ask_price']
#        ask_size = HarryHoodData['ask_size']
        bid_price = HarryHoodData['bid_price']
#        bid_size = HarryHoodData['bid_size']
        date = HarryHoodData['updated_at']
#        close =HarryHoodData['previous_close']
        TodayStockData.append([symbol, bid_price, ask_price, date])
    return(TodayStockData)        
    
