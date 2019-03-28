# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 22:10:47 2018

@author: Eric Bell
"""

import db_loadfiles.config as config
import tweepy


from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures 
import itertools
from nltk.tokenize import WordPunctTokenizer
from bs4 import BeautifulSoup
import re

import time
from nltk.corpus import stopwords
#from GetDataHistoric import GetCompanyNames
consumer_key = config.consumer_key
consumer_secret = config.consumer_secret
access_key = config.access_token
access_secret = config.access_token_secret

tok = WordPunctTokenizer()
pat1 = r'@[A-Za-z0-9]+'
pat2 = r'https?://[A-Za-z0-9./]+'
combined_pat = r'|'.join((pat1, pat2))


def tweet_cleaner(text):
    soup = BeautifulSoup(text, 'lxml')
    souped = soup.get_text()
    stripped = re.sub(combined_pat, '', souped)
    try:
        clean = stripped.decode("utf-8-sig").replace(u"\ufffd", "?")
    except:
        clean = stripped
    lo = re.sub("'", " ", clean)
    letters_only = re.sub("[^a-zA-Z]", " ", lo)
    
    lower_case = letters_only.lower()
    # During the letters_only process two lines above, it has created unnecessay white spaces,
    # I will tokenize and join together to remove unneccessary white spaces
    words = tok.tokenize(lower_case)
    return (" ".join(words)).strip()

def bigram_word_feats_stopwords(words, score_fn=BigramAssocMeasures.chi_sq, n=200):
    stopset = set(stopwords.words('english')) - set(('over', 'under', 'below', 'more', 'most', 'no', 'not', 'only', 'such', 'few', 'so', 's', 'too', 'very', 'just', 'any', 'once'))      
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)   
    return dict([(ngram, True) for ngram in itertools.chain(words, bigrams) if ngram not in stopset])
  


def stopword_filtered_word_feats(words):
    stopset = set(stopwords.words('english')) - set(('over', 'under', 'below', 'more', 'most', 'no', 'not', 'only', 'such', 'few', 'so', 's', 'too', 'very', 'just', 'any', 'once'))      

    return ([(word) for word in words if word not in stopset])

def get_tweets_hashtag(hashtag):
    
#    time.sleep(20)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    time.sleep(20)
    MAX_TWEETS =   5
    outtweets = []
    for tweet in tweepy.Cursor(api.search, q=hashtag , rpp=100).items(MAX_TWEETS):
        id_str = tweet.id_str
        text = tweet_cleaner(tweet.text.encode('utf-8'))
        
        date =  tweet.created_at
#        split_words = text.split()
#        StopWords = stopword_filtered_word_feats(split_words)
#        WordFeats= bigram_word_feats_stopwords(StopWords)
        
        outtweets.append([id_str, text ,date])
                              
    return(outtweets)
#    
#    
#get_tweets_hashtag('CNNX')
#get_tweets_screenname('MarijuanaStock_')


def get_tweets_screenname(screen_name):
 
    time.sleep(10)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
 
    all_the_tweets = []

    new_tweets = api.user_timeline(screen_name=screen_name, count=100)
 
    all_the_tweets.extend(new_tweets)
 
    # save id of 1 less than the oldest tweet
 
    oldest_tweet = all_the_tweets[-1].id - 1
 
    while len(new_tweets) > 0:
        # The max_id param will be used subsequently to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name,
                count=200, max_id=oldest_tweet)
 
        all_the_tweets.extend(new_tweets)
 
        # id is updated to oldest tweet - 1 to keep track
 
        oldest_tweet = all_the_tweets[-1].id - 1
        print ('...%s tweets have been downloaded so far' % len(all_the_tweets))
#    outtweets = [[tweet.id_str, tweet.created_at,
#                 tweet.text.encode('utf-8')] for tweet in all_the_tweets]
    outtweets =[]
    for tweet in all_the_tweets:
        tweet.id_str
        tweet.created_at
        text = tweet_cleaner(tweet.text.encode('utf-8'))
        outtweets.append([tweet.id_str, tweet.created_at, text ])
#    outtweets = [[tweet.id_str, tweet.created_at,
#                 tweet.text.encode('utf-8')] for tweet in all_the_tweets]
    
    return(outtweets) 

#get_tweets_screenname('MarijuanaStock_')
