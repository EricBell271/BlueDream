# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 19:10:04 2018

@author: Eric Bell
"""
from SupportLevels import SupportLevels, ResistanceLevels
from DataBaseQuery import GetPrice
    
import numpy as np
from trendy import segtrends, gentrends, iterlines, supres
from CalculateMovingAverages import CalulateResistance,CalulateSupport

    
from db_loadfiles.connect_DB import BlueDream


price = GetPrice(Database = BlueDream)	

#SL  = SLevels 
#SL  = SLevels 
SLevels = SupportLevels(PricingData = price)

RLevels = ResistanceLevels(PricingData = price)
r= CalulateResistance(RLevels)

s= CalulateSupport(SLevels)

def GetLastSupportLevel(x):
    Array = []
    for i in range(len(x)):
        
#        ticker = x[i][0]
#        date = x[i][1]
        r3 = x[i][3]
        Array.append(r3)
    return(Array)

def GetPriceLevel(x):
    Array = []
    for i in range(len(x)):
        
#        ticker = x[i][0]
#        date = x[i][1]
        p = x[i][4]
        Array.append(p)
    return(Array)


def GetLastResistanceLevel(x):
    Array = []
    for i in range(len(x)):
        
#        ticker = x[i][0]
#        date = x[i][1]
        p = x[i][4]
        Array.append(p)
    return(Array)

def GetTickerDate(x):
    Array = []
    for i in range(len(x)):
        ticker = x[i][0]
        date = x[i][1]
        Array.append([ticker , date])
    return(Array)
    
    
support= GetLastSupportLevel(s)   
resistance = GetLastResistanceLevel(r) 
p = GetPriceLevel(s)


supres(np.array(p), n = 20)
#supres(np.array(support), n = 20)
#supres(np.array(resistance), n = 20)


segtrends(np.array(p), segments=2, charts=True)

gentrends(np.array(p), window=1/30.0, charts=True)
import pandas as pd
r= pd.DataFrame(r)
s= pd.DataFrame(s)
r.plot()

SLevels = SupportLevels(PricingData = price)
p =  pd.DataFrame(SLevels )
r =  pd.DataFrame(RLevels )
s.plot()
p.plot()
r.plot()
#segtrends(np.array(support), segments=3, charts=True)
#segtrends(np.array(resistance), segments=3, charts=True)
#


  



#
#import matplotlib.pyplot as plt






#from scipy.signal import argrelextrema

#
#
#maxInd = argrelextrema(x, np.greater)
#
#y[maxInd]
#
#


#
#
#
#

#minm=np.array([],dtype=int)
#maxm=np.array([],dtype=int)
#length = y.size
#i=0
#
#while i < length-1:
#    if i < length - 1:
#        while i < length-1 and y[i+1] >= y[i]:
#            i+=1
#
#        if i != 0 and i < length-1:
#            maxm = np.append(maxm,i)
#
#        i+=1
#
#    if i < length - 1:
#        while i < length-1 and y[i+1] <= y[i]:
#            i+=1
#
#        if i < length-1:
#            minm = np.append(minm,i)
#        i+=1
#
#
#print(minm)
#print(maxm)
#
#
#
#  
#df_R =pd.DataFrame(GetPrice(BlueDream))

