# import required packages
import os
import time
from dotenv import load_dotenv
import tweepy
import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
from textblob import TextBlob
import nltk
import string
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from sklearn.feature_extraction.text import CountVectorizer

# Import NLTK lexicon
nltk.download("vader_lexicon")
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("omw-1.4")


# Load API Keys from .env file and create API object
load_dotenv()

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Retrieve Tweets by Username
def get_tweets_by_username(username, count):

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


# Retrieve Tweets by Hashtag(s) / Keyword(s)
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
    data_df = pd.DataFrame(data)
    return data_df


# Sidebar to choose to retrieve either Tweets by Username or Hashtag/Phrase
st.sidebar.title("Select the type of data you want to retrieve")
st.sidebar.subheader("Instructions:")
st.sidebar.markdown(
    """
    - Select the type of data you want to retrieve
    - Enter hashtag(s) or phrase(s) to retrieve from Twitter
    - Separate multiple hashtags or phrases with a comma
    - Enter a number of tweets to retrieve (1 - 1000)
    """
)
selection = st.sidebar.selectbox(
    "Select the type of data you want to retrieve", ["Username", "Hashtag/Phrase"]
)

# Retrieve Tweets by Username / Hashtag(s) / Keyword(s)
st.header("Tweet Sentiment Analysis")

try:
    if selection == "Username":
        username = st.text_input("Enter the username to retrieve tweets from:")
        print(username)
        num_tweets = st.slider(
            "Select number of tweets to be retrieved:", 0, 1000, 100, 100
        )
        if st.button("Retrieve Tweets"):
            tweets_df = get_tweets_by_username(username, num_tweets)
            st.markdown(
                """
        #### Summary of Tweets Retrieved
        """
            )
            st.write(tweets_df.shape[0], "tweets retrieved")
            st.write(tweets_df.shape[1], "columns retrieved")
            st.table(tweets_df.head())

    else:
        keywords = st.text_input(
            "Enter the hashtag(s) or phrase(s) to retrieve from Twitter:"
        )
        num_tweets = st.slider(
            "Select number of tweets to be retrieved:", 0, 1000, 100, 100
        )
        keywords = list(set(keywords.split(",")))
        if st.button("Retrieve Tweets"):
            tweets_df = get_tweets_by_search_term(keywords, num_tweets)
            st.markdown(
                """
        #### Summary of Tweets Retrieved
        """
            )
            st.write(tweets_df.shape[0], "tweets retrieved")
            st.write(tweets_df.shape[1], "columns retrieved")
            st.table(tweets_df.head())
except BaseException as e:
    st.error(
        f"Something went wrong: Make sure you have entered a valid username or hashtag/phrase without any special characters"
    )
    pass

# Sentiment Analysis
