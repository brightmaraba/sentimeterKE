import os
import time
from dotenv import load_dotenv
import tweepy
import pandas as pd


load_dotenv()

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)


username = "LibranTechie"
count = 100


def get_tweets_by_username(username, count):

    try:
        tweets = api.user_timeline(
            screen_name=username, count=count, language="en", tweet_mode="extended"
        )
        tweets_list = [[tweet.created_at, tweet.user_id, tweet.text] for tweet in tweets]
        tweets_df = pd.DataFrame(tweets_list, columns=["Datetime", "Tweet_ID", "Tweet"])
        this_file_path = os.path.abspath(__file__)
        BASE_DIR = os.path.dirname(this_file_path)
        tweets_file_name = os.path.join(BASE_DIR, "tweets", "tweets.pkl")
        tweets_df.to_pickle(tweets_file_name)
        return tweets_df
    except BaseException as e:
        print("failed on_status,", str(e))
        time.sleep(3)


def get_tweets_by_search_term(search_term=["RejectBBI"]):
    data = []
    counter = 0
    for tweet in tweepy.Cursor(
        api.search_tweets,
        q='"{}" -filter:retweets'.format(search_term),
        count=5000,
        lang="en",
        tweet_mode="extended",
    ).items():
        tweet_details = {}
        tweet_details["UserId"] = tweet.user.name
        tweet_details["TweetId"] = tweet.id
        tweet_details["tweet"] = tweet.full_text
        tweet_details["location"] = tweet.user.location
        tweet_details["created"] = tweet.created_at.strftime("%d-%b-%Y")
        data.append(tweet_details)
        counter += 1
        if counter == 5000:
            break
        else:
            pass
    data_df = pd.DataFrame(data)
    this_file_path = os.path.abspath(__file__)
    BASE_DIR = os.path.dirname(this_file_path)
    tweet_list_file_name = os.path.join(BASE_DIR, "tweets", "tweet_list.pkl")
    data_df.to_pickle(tweet_list_file_name)
    return data_df
