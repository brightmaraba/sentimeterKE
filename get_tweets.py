import os
from fastapi import FastAPI
import time
from dotenv import load_dotenv
import tweepy
import pandas as pd
import json

load_dotenv()
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

auth =  tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)


username = 'LibranTechie'
count = 50

def get_tweets_by_username(username, count):

    try:
        tweets = tweepy.Cursor(api.user_timeline,id=username).items(count)
        tweets_list = [[tweet.created_at, tweet.id, tweet.text] for tweet in tweets]
        tweets_df = pd.DataFrame(tweets_list, columns=['Datetime', 'Tweet_ID', 'Tweet'])
        this_file_path = os.path.abspath(__file__)
        BASE_DIR = os.path.dirname(this_file_path)
        ENTIRE_PROJECT_DIR = os.path.dirname(BASE_DIR)
        tweets_file_name = os.path.join(BASE_DIR, "tweets", "tweets.csv")
        tweets_df.to_csv(tweets_file_name, header=True)
        return tweets_df
    except BaseException as e:
            print('failed on_status,',str(e))
            time.sleep(3)

def get_tweets_by_search_term(search_term="RejectBBI"):
    assert isinstance(search_term, list)
    data = []
    counter = 0
    for tweet in tweepy.Cursor(api.search, q='\"{}\" -filter:retweets'.format(search_term), count=100, lang='en', tweet_mode='extended').items():
        tweet_details = {}
        tweet_details['name'] = tweet.user.screen_name
        tweet_details['tweet'] = tweet.full_text
        tweet_details['retweets'] = tweet.retweet_count
        tweet_details['location'] = tweet.user.location
        tweet_details['created'] = tweet.created_at.strftime("%d-%b-%Y")
        tweet_details['followers'] = tweet.user.followers_count
        tweet_details['is_user_verified'] = tweet.user.verified

        data.append(tweet_details)
        counter += 1
        if counter == 10000:
            break
        else:
            pass
    data_df = pd.DataFrame(data)
    this_file_path = os.path.abspath(__file__)
    BASE_DIR = os.path.dirname(this_file_path)
    ENTIRE_PROJECT_DIR = os.path.dirname(BASE_DIR)
    tweet_list_file_name = os.path.join(BASE_DIR, "tweets", "tweet_list.csv")
    data_df.to_csv(tweet_list_file_name, header=True)
    return data_df
    print('Done!')


