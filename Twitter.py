import pandas as pd
import tweepy
from textblob import TextBlob
import preprocessor as p
import nltk
import re
import string
from csv import writer



credentials = pd.read_csv("credentials.csv", sep=";")
AccessToken = credentials['Key'][0]
AccessTokenSecret = credentials['Key'][1]
ApiKey = credentials['Key'][2]  # = consumerKey
ApiSecretKey = credentials['Key'][3]  # = consumerSecret


# create authenticate object and set tokens
authenticate = tweepy.OAuthHandler(ApiKey, ApiSecretKey)
authenticate.set_access_token(AccessToken, AccessTokenSecret)
api = tweepy.API(authenticate, wait_on_rate_limit=True)


def clean_txt(text):
  #  text = text.replace('|', ' ')
    text = text.replace('\n', ' ')
    text = text.replace('\n\n', ' ')


    
    return text

def get_status(text):
    return api.get_status()

def get_subjectivity(text):
    return TextBlob(text).sentiment.subjectivity

def get_polarity(text):
    return TextBlob(text).sentiment.polarity


def get_influencer_tweets(name, count):
    posts = api.user_timeline(screen_name=name, count=count, lang="en", tweet_mode="extended")

    df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])
    df['Tweets'] = df['Tweets'].apply(clean_txt)
    df['Subjectivity'] = df["Tweets"].apply(get_subjectivity)
    df['Polarity'] = df['Tweets'].apply(get_polarity)
    return df

def get_tweets_by_hashtags(hashtag, date="2020-01-01",nums=20):
    hashtag += " -filter:retweets"
    tweets = tweepy.Cursor(api.search, q=hashtag, lang="en", since=date,tweet_mode="extended").items(nums)
    hashtag_info = [[tweet.full_text,tweet.user.screen_name, tweet.user.location, tweet.user.followers_count,
                    tweet.user.friends_count,tweet.user.statuses_count,tweet.user.created_at,tweet.user.description,
                    tweet.user.verified, tweet.user.favourites_count]
                    for tweet in tweets]

    df_hashtag = pd.DataFrame(data=hashtag_info,columns=['Tweets','User','Location','Follower Count','Following Count',
                                                        'Number of Tweets','Account Created Date','Account Description',
                                                        'Verified','Favourites Count'])
    df_hashtag['Tweets'] = df_hashtag['Tweets'].apply(clean_txt)
    df_hashtag['Account Description'] = df_hashtag['Account Description'].apply(clean_txt)
    df_hashtag['Subjectivity'] = df_hashtag['Tweets'].apply(get_subjectivity)
    df_hashtag['Polarity'] = df_hashtag['Tweets'].apply(get_polarity)
    return df_hashtag
    append_list_as_row("hashtag_tweets.csv",df_hashtag)


#get_influencer_tweets("@realDonaldTrump", 50).to_csv('Trump_Tweets.csv')

#if file already exists in folder --> header=False
get_tweets_by_hashtags("#blacklivesmatter").to_csv("hashtag_tweets.csv", mode='a', header=False, index=False)
