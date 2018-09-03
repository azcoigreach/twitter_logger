#!/usr/bin/env python
__project__ = 'Twitter Stream Query'
__author__  = 'azcoigreach@gmail.com'

# To run this code, first edit config.py

import sys
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
from datetime import datetime
import dateutil.parser
import argparse
import string
import config
import json
from pymongo import MongoClient
from unidecode import unidecode
from textblob import TextBlob
import logging
import coloredlogs
from colorama import init, Fore
coloredlogs.install(level='DEBUG')
logger = logging.getLogger('TWITTER LOGGER')
logger.setLevel(logging.INFO)

MONGO_SERVER= str(config.MONGO_HOST + '/' + config.MONGO_DB)
COLLECTION = config.MONGO_COL
WORDS = config.STREAM_FILTER

class StreamListener(tweepy.StreamListener):    
 
    def on_connect(self):
        logger.warning(Fore.YELLOW + "You are now connected to the streaming API.")
 
    def on_error(self, status_code):
        logger.error(Fore.RED + 'An Error has occured: ' + repr(status_code))
        return False
 
    def on_data(self, data):
        try:
            client = MongoClient(MONGO_SERVER)
            db = client.twitter_stream
            datajson = json.loads(data)
            if not datajson['text'].startswith('RT'):
                iso_date = dateutil.parser.parse(datajson['created_at'])
                datajson['created_at'] = iso_date
                tweet_text = unidecode(datajson['text'])
                analysis = TextBlob(tweet)
                datajson = analysis.sentiment.polarity
                sentiment_subjectivity = analysis.sentiment.subjectivity
                datajson['sentiment']['polarity'] = sentiment_polarity
                datajson['sentiment']['subjectivity'] = sentiment_subjectivity
                db.twitter_query.insert(datajson)
                logger.info(Fore.CYAN + "Tweet collected at " + str(iso_date.strftime('%a %b %d %H:%M:%S +0000 %Y')) + Fore.LIGHTCYAN_EX + ' ' + str(tweet_text))
                
        except Exception as err:
           logger.error(Fore.RED + 'Stream Error: %s', err)
           


while True:
    try:
        auth = OAuthHandler(config.consumer_key, config.consumer_secret)
        auth.set_access_token(config.access_token, config.access_secret)
        listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True)) 
        streamer = tweepy.Stream(auth=auth, listener=listener)
        logger.warning(Fore.YELLOW + "Tracking: " + str(WORDS))
        streamer.filter(track=WORDS)
    except KeyboardInterrupt:
        logger.error(Fore.RED + 'exiting...')
        sys.exit(-1)
    except Exception as err:
        logger.error(Fore.RED + "Error main: %s", err)
        time.sleep(5)
        continue
    