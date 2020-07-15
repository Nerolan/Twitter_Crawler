import pandas as pd
import numpy as np
import tweepy
from tweepy import Stream
from tweepy import StreamListener
import json
from textblob import TextBlob
import re
import csv


credentials = pd.read_csv("credentials.csv", sep=";")
AccessToken = credentials['Key'][0]
AccessTokenSecret = credentials['Key'][1]
ApiKey = credentials['Key'][2]  # = consumerKey
ApiSecretKey = credentials['Key'][3]  # = consumerSecret

auth = tweepy.OAuthHandler(ApiKey, ApiSecretKey)
auth.set_access_token(AccessToken, AccessTokenSecret)

api = tweepy.API(auth)

trump = 0
biden = 0

header_name = ['Trump','Biden']
with open('trump_biden_sentiment.csv','w') as file:
    writer = csv.DictWriter(file,fieldnames=header_name)
    writer.writeheader()


class Listener(StreamListener):

    def on_data(self, data):
        raw_tweets = json.loads(data)
        try:
            tweets = raw_tweets['text']
            tweets = ' '.join(re.sub("(@[A-Za-z0-9]+) | ([^0-9A-Za-z \t]) | (\w+:\/\/\S+)"," ",tweets).split())
            tweets = ' '.join(re.sub('RT',' ',tweets).split())

            blob = TextBlob(tweets.strip())

            global trump
            global biden

            trump_sentiment = 0
            biden_sentiment = 0

            for sent in blob.sentences:
                if "Trump" in sent and "Biden" not in sent:
                    trump_sentiment = trump_sentiment + sent.sentiment.polarity
                else:
                    biden_sentiment = biden_sentiment + sent.sentiment.polarity

            trump = trump + trump_sentiment
            biden = biden + biden_sentiment

            with open('trump_biden_sentiment.csv','a') as file:
                writer = csv.DictWriter(file,fieldnames=header_name)
                info = {
                    'Trump': trump,
                    'Biden': biden
                }
                writer.writerow(info)

            print(tweets)
            print()
        except:
            print(f"Error!!-- Workin on the weekend like usual")

    def on_error(self,status):
        print(status)


twitter_stream = Stream(auth, Listener())
twitter_stream.filter(track= ['Trump','Biden'])
