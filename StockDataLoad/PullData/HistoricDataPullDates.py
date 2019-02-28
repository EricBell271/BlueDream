# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 22:17:15 2019

@author: Eric Bell
"""

from datetime import datetime as dt, timedelta


def GetTodaysDate():
    days_to_subtract = 0
    d = (dt.today() - timedelta(days=days_to_subtract))
    last_date = d.strftime('%Y-%m-%d')
    return(last_date)
#GetTodaysDate()
    
def GetYearWindow():
    window_length = 365
    d = (dt.today() - timedelta(days=window_length ))
    window_begin = d.strftime('%Y-%m-%d')
    return(window_begin)
#    
#GetYearWindow()