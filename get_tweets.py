import os
import tweepy
import numpy as np
import pandas as pd
from dotenv import load_dotenv

# Load API Keys from .env file and create API object
load_dotenv()

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Function to retrieve Tweets by Username
def get_tweets_by_username(username, count=1):

    tweets = api.user_timeline(
        screen_name=username, count=count, language="en", tweet_mode="extended"
    )
    tweets_list = [
        [
            tweet.user.name,
            tweet.full_text,
            tweet.user.location,
            tweet.created_at.strftime("%d-%b-%Y"),
        ]
        for tweet in tweets
    ]
    tweets_df = pd.DataFrame(
        tweets_list,
        columns=["user_id", "tweet", "location", "created_at"],
    )
    return tweets_df


# Function to retrieve Tweets by Hashtag(s) / Keyword(s)
def get_tweets_by_search_term(keywords, num_tweets):
    data = []
    counter = 0
    for tweet in tweepy.Cursor(
        api.search_tweets,
        q='"{}" -filter:retweets'.format(keywords),
        count=num_tweets,
        lang="en",
        tweet_mode="extended",
    ).items():
        tweet_details = {}
        tweet_details["user_id"] = tweet.user.name
        tweet_details["tweet"] = tweet.full_text
        tweet_details["location"] = tweet.user.location
        tweet_details["created_at"] = tweet.created_at.strftime("%d-%b-%Y")
        data.append(tweet_details)
        counter += 1
        if counter == num_tweets:
            break
        else:
            pass
    tweets_df = pd.DataFrame(data)
    return tweets_df
