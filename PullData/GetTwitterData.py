
"""
Created on Sat Sep 29 22:20:37 2018

@author: Eric Bell
"""


from PullData.get_tweets import get_tweets_hashtag, get_tweets_screenname
from db_loadfiles.connect_DB import BlueDream
#from PullData.GetDataHistoric import GetTickerNames
from UniverseData.universe import Faber_Ticker, SPY_Only_Universe


import time
from textblob import TextBlob

#import csv
#from DataBaseQuery import  GetCompanyNames

#universe = SPY_Only_Universe

def get_tweet_sentiment(tweet):
    sentiment = TextBlob(tweet)
    score = sentiment.sentiment.polarity
    if score > 0:
        return 'positive'
    elif score == 0:
        return 'neutral'
    elif score < 0:
        return 'negative'

def CreateTwitterLoadTable(DataBase):
    DB = DataBase

    cursor = DB.cursor()

    table_name = "TickerDateText"
    cursor.execute("DROP TABLE IF EXISTS " + table_name)
    cursor.execute("""
                   CREATE TABLE {} (
            no  VARCHAR(20) , 
           ticker VARCHAR(200),
           Date VARCHAR(20),
           Text VARCHAR(300),
            Sentament VARCHAR(20), 
            DateTime VARCHAR(20)
	);   
    """.format(table_name))
    DB.commit()   

CreateTwitterLoadTable(BlueDream)

def AnalysisDBInsert(issue) :
    print('The current Ticker : ' , issue[1:])
    start = time.clock()
    ticker = issue[1:]
    output = get_tweets_hashtag(issue)
#    output = get_tweets_screenname(issue)

    DB = BlueDream            
    cursor = DB.cursor()
    for row in output:
        row

        table_name = "TickerDateText"
        id_str = row[0]
        DateTime = row[2]
        Date = DateTime.strftime('%Y-%m-%d')
        TweetText =row[1]
        
        print(TweetText)
        Sentament =get_tweet_sentiment(str(TweetText))
        cursor.execute("""
                     INSERT INTO {}( no ,ticker, Date, Text, Sentament, DateTime)
                       VALUES('{}','{}', '{}', '{}', '{}', '{}')
	""".format(
        		table_name,
                id_str,
                ticker, 
                Date, 
                TweetText,
                Sentament,
                DateTime
       
	))
    DB.commit()   
    end = time.clock()
    print(end-start)
#def Insert_MultipleIssues():
#    file_path = '..\AnalyzeTwitter\data\issue.csv'
#    with open(file_path) as csvDataFile:
#        csvReader = csv.reader(csvDataFile)
#        for row in csvReader:
#            print(row[0])
#            AnalysisDBInsert(row[0])
#
#Insert_MultipleIssues()


#
def InsertHashtagData(universe):

    hashtags = universe[:]
    len(hashtags)
#    hashtags = GetCompanyNames(BlueDream)
    for s in hashtags :
        ticker = '$' + s
        print(ticker)
        AnalysisDBInsert(ticker)

##AnalysisDBInsert('#CRBP') 
#
#search_hashtags()
#