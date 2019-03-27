# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 18:37:41 2018

@author: Eric Bell
"""

import numpy as np
from DataBaseQuery import GetPrice
from numpy import convolve
import matplotlib.pyplot as plt
from db_loadfiles.connect_DB import BlueDream 

#def movingaverage (values, window):
#    weights = np.repeat(1.0, window)/window
#    sma = np.convolve(values, weights, 'valid')
#    return(sma)
 
def PP(H, L, C):
	pp = (H+L+C)/3
	return(pp)
	 #(Pivot Point * 2) - High
def S1(P, H):
	S1= (P*2) - H
	return(S1)
def S2(P, H, L):
	S2= (P - (H - L) )
	# Pivot Point - (High - Low)
	return(S2)

def S3(P, H, L):
	S3=L-(2*(H-P))
#	Low - 2 * (High - Pivot Point)
	return(S3)
	
def R1(P, L):
	R1= (P*2) - L
	#(Pivot Point * 2) - Low.
	return(R1)

def R2(P, H, L):
	R2= (P + (H - L) )
	# Pivot Point + ( High - Low)
	return(R2)

def R3(P, H, L):
	R3=H + (2*(P-L))
#	High + 2 * (Pivot Point - Low)
	return(R3)
#    
#
price = GetPrice(Database = BlueDream)	

def SupportLevels(PricingData):
    SupportLevels= []

    for i in PricingData :
        t = i[0]
        d = i[1]
        close =i[2]
        high = i[3]
        low = i[4]
        pp = PP(high, low, close)
        support1 =  S1(pp, high)
        support2 =  S2(pp, high, low)
        support3 = 	S3(pp, high, low)
        SupportLevels.append({'ticker' : t, 'date' :d,   's1' : support1, 's2' : support2, 's3' : support3})

    return(SupportLevels)
#
SupportLevels(price)



def ResistanceLevels(PricingData):
    ResistanceLevels = []
    for i in PricingData :
        t = i[0]
        d = i[1]
        close =i[2]
        high = i[3]
        low = i[4]
        pp = PP(high, low, close)	        
        resistance1 =  R1(pp,low)
        resistance2 =  R2(pp, high, low)
        resistance3 = 	R3(pp, high, low)
        ResistanceLevels.append({ 'ticker' : t ,'date' :d,  'r1' : resistance1, 'r2' : resistance2, 'r3' : resistance3})
    return(ResistanceLevels)




