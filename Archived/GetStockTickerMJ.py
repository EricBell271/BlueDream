# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 16:24:41 2018

@author: Eric Bell
"""


import requests
from bs4 import BeautifulSoup
from itertools import zip_longest

from db_loadfiles.connect_DB import BlueDream
from re import sub
DB = BlueDream
def LegalizeIt():

    url = "https://marijuanaindex.com/marijuana-stock-universe/"
    page = requests.get(url).text
    soup = BeautifulSoup(page,'lxml')
    tab_data = []
    for rowdata in soup.find_all("tr"):
        for celldata in rowdata.find_all(["td"]):
            tab_data.append(celldata.text)
    tab_data = [[celldata.text for celldata in rowdata.find_all(["td"])]
                        for rowdata in soup.find_all("tr")]

    m1 = [s for s in tab_data if len(s) != 1 ]
    m2 = [s for s in m1 if len(s) != 2 ]
    mj_ticker=  [s for s in m2 if s ]
    
    MJdata = []

    for i in range(len(mj_ticker)) :
#        mj_ticker[i][4] 
        name = mj_ticker[i][1]
#        :.*
        t = mj_ticker[i][2]

        ticker = sub(r':.*', '', t)       
#        print(ticker)
        price = mj_ticker[i][3]
#        PCTChange = mj_ticker[i][4]
        volume = mj_ticker[i][5]
        Dividend= mj_ticker[i][6]
        Exchange =mj_ticker[i][8]
        MKTCap = mj_ticker[i][7]
        sector = mj_ticker[i][9]
        MJdata.append([name, ticker,  MKTCap , volume, price ,Dividend, Exchange, sector] )
        
    
    cursor = DB.cursor()
    table_name = "TickerName"
    cursor.execute("DROP TABLE IF EXISTS " + table_name)
    cursor.execute("""
                   CREATE TABLE {} (
                   

           CompanyName VARCHAR(200),
           Ticker VARCHAR(30),
           MKTCap VARCHAR(50),
           Volume VARCHAR(50),
           Price VARCHAR(50),
           Dividend VARCHAR(5), 
           Exchange VARCHAR(20),
           Sector VARCHAR(30)

           
	);   
    """.format(table_name))
             
#    args_str = ','.join( str(x)  for x in mj_ticker)
#    (cursor.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s, %s,%s,%s,%s)", args_str))
#    cursor.execute("INSERT INTO  MJ_Ticker  VALUES " + args_str) 
 
    cursor.executemany("INSERT INTO TickerName VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", MJdata)

    DB.commit()





