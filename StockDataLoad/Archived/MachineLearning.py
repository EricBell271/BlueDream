# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 19:50:09 2018

@author: Eric Bell
"""


from DataBaseQuery import GetSentimentPriceDatePositive, GetSentimentPriceDateNegative
from db_loadfiles.connect_DB import BlueDream
#from db_loadfiles.connect_DB import BlueDream
posfeats  = GetSentimentPriceDatePositive(BlueDream)
negfeats  = GetSentimentPriceDateNegative(BlueDream)


 


for s in posfeats, negfeats:

    ticker = s[0]
    date =  s[1]
    price =s[2]
#    volume=s[3]
    UserName= s[4]
    Tweet = s[5]

    sentiment = s[6] 
    negcutoff = len(negfeats)*3/4
    poscutoff = len(posfeats)*3/4
    trainfeats = negfeats[:int(negcutoff)] + posfeats[:int(poscutoff)]
    len(trainfeats)
    testfeats = negfeats[int(negcutoff):] + posfeats[int(poscutoff):]
    len(testfeats)