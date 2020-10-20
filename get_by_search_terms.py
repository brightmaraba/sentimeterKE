import os
from time import time
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


this_file_path = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(this_file_path)
ENTIRE_PROJECT_DIR = os.path.dirname(BASE_DIR)
file_name = os.path.join(BASE_DIR, "tweets", "tweet_list.csv")

def get_tweets_by_search_term(search_term):
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
        if counter == 1000:
            break
        else:
            pass
    with open('tweets/{}.json'.format(search_term), 'w') as f:
        json.dump(data, f)
    data_df = pd.DataFrame(data)
    data_df.to_csv(file_name, header=True)
    print('Done!')


if __name__ == "__main__":
    get_tweets = get_tweets_by_search_term(search_term=["Ruto", "TangaTanga"])