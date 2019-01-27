# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 18:17:28 2018

@author: Eric Bell
"""

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

def CreateSRLevelLoadTable(DataBase):
    DB = DataBase

    cursor = DB.cursor()

    table_name = "TickerDateSupportResistance"
    cursor.execute("DROP TABLE IF EXISTS " + table_name)
    cursor.execute("""
                   CREATE TABLE {} (
            no  VARCHAR(20) , 
           ticker VARCHAR(200),
           Date VARCHAR(20),
           Text VARCHAR(300),
            Support1 REAL, 
            Support2 REAL,
            Support3 REAL,
            Resistance1 REAL,
            Resistance2 REAL,
            Resistance3 REAL
	);   
    """.format(table_name))
    DB.commit()   

CreateSRLevelLoadTable(BlueDream)
 
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

def AllLevels(PricingData):
#    AllLevels= []

    for i in PricingData :
        ticker = i[0]
        Date = i[1]
        close =i[2]
        high = i[3]
        low = i[4]
        pp = PP(high, low, close)
        support1 =  S1(pp, high)
        support2 =  S2(pp, high, low)
        support3 = 	S3(pp, high, low)
        resistance1 =  R1(pp,low)
        resistance2 =  R2(pp, high, low)
        resistance3 = 	R3(pp, high, low)
        DB = BlueDream
        cursor = DB.cursor()
        table_name = 'TickerDateSupportResistance'
        cursor.execute("""
                     INSERT INTO {}(ticker, Date, 
                     Support1,
                     Support2,
                     Support3 ,
                     Resistance1,
                     Resistance2,
                     Resistance3
                     
                     )
                       VALUES('{}','{}', {}, {}, {}, {}, {}, {})
	""".format(
        		table_name,
                ticker, 
                Date, 
                support1,
                support2,
                support3 ,
                resistance1,
                resistance2,
                resistance3
       
	))
    try :    
        DB.commit()
        print('DataCommitted')
        return(0)
    except :
        DB.rollback()
        print('Transaction Not Committed')
        return(1)
AllLevels(price)