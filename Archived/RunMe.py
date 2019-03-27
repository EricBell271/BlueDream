# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 20:44:34 2018

@author: Eric Bell
"""


from GetStockTickerMJ import LegalizeIt
from GetDataHistoric import HistoricalPricingInsert
from GetTwitterData import Insert_MultipleIssues
from GetDataToday import TodayPricingInsert
if __name__ == '__main__':
    print('Getting Tickers')
    LegalizeIt()
    print('Insert UserNames')
    Insert_MultipleIssues()
    print('Insert Pricing')
    HistoricalPricingInsert()  