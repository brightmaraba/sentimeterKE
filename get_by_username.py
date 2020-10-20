import os
import time
from dotenv import load_dotenv
import tweepy
import pandas as pd

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
file_name = os.path.join(BASE_DIR, "tweets", "tweets.csv")

username = ''
count = 50

def get_tweets_by_username(username, count):

    try:
        tweets = tweepy.Cursor(api.user_timeline,id=username).items(count)
        tweets_list = [[tweet.created_at, tweet.id, tweet.text] for tweet in tweets]
        tweets_df = pd.DataFrame(tweets_list, columns=['Datetime', 'Tweet_ID', 'Tweet'])
        tweets_df.to_csv(file_name, header=True)
        return tweets_df
    except BaseException as e:
            print('failed on_status,',str(e))
            time.sleep(3)

if __name__ == "__main__":
    get_tweets = get_tweets_by_username("girlfromtherift", 50)