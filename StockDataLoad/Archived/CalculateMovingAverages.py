# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 20:23:30 2018

@author: Eric Bell
"""

#from SupportLevels import SupportLevels, ResistanceLevels
#from DataBaseQuery import GetPrice
##    
#from db_loadfiles.connect_DB import BlueDream


def moving_average(mylist):
    N = 30
    cumsum, moving_aves = [0], []
    for i, x in enumerate(mylist, 1):
        cumsum.append(cumsum[i-1] + x)
        if i>=N:
            moving_ave = (cumsum[i] - cumsum[i-N])/N
        #can do stuff with moving_ave here
            moving_aves.append(moving_ave)
    return(moving_aves)

#price = GetPrice(Database = BlueDream)	

#SLevels = SupportLevels(PricingData = price)
#SL= SLevels
def CalulateSupport(SL):
    s1=[]
    s2=[]
    s3=[]
    close = []
    date = []
    ticker =[]
    for i in SL:
        s1.append(i['s1'])
#        len(createWindow(s1))
        s2.append(i['s2'])
        s3.append(i['s3'])
        ma_s1= moving_average(s1)
        ma_s2= moving_average(s2)
        ma_s3= moving_average(s3)
        close.append(i['close'])
        date.append(i['date'])
        ticker.append(i['ticker'])
    return([[i, j, k, y , z, w] for i, j, k, y, z, w in zip(ticker, date, ma_s1, ma_s2,  ma_s3, close)])
#CalulateSupport(SLevels)

def CalulateResistance(RL):
    r1=[]
    r2=[]
    r3=[]
    date = []
    ticker =[]
    for i in RL:
        print(i)
        r1.append(i['r1'])
        r2.append(i['r2'])
        r3.append(i['r3'])
        date.append(i['date'])
        ticker.append(i['ticker'])
        ma_r1= moving_average(r1)
        ma_r2= moving_average(r2)
        ma_r3= moving_average(r3)
    return([[i, j, k, y , z] for i, j, k, y, z in zip(ticker, date, ma_r1, ma_r2,  ma_r3)])
    
##
###215-186
#r = CalulateResistance(RLevels)
#
#len(r) 
#s = CalulateSupport(SLevels)
#len(s)
#
#
#type(r)
#
#
##
#for i in r :
#    print(i)

#
#


