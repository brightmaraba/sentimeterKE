# import required packages
import os
import re
import time
import nltk
import string
import tweepy
import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
from textblob import TextBlob

# Styling to hide menu
hide_menu = """
<style>
    #MainMenu {
        visibility: hidden;
        }
    footer {
        visibility: visible;
        }
    footer:after {
        content: "Copyright © 2022 - @LibranTechie | All rights reserved | Powered by Python | ";
        display: block;
        position: relative;
        color: tomato;
        align-items: center;
    }
</style>
"""

st.markdown(hide_menu, unsafe_allow_html=True)


# from dotenv import load_dotenv
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

# Import NLTK lexicon
nltk.download("vader_lexicon")
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("omw-1.4")

# Load API Secrets and create API object


consumer_key = st.secrets["CONSUMER_KEY"]
consumer_secret = st.secrets["CONSUMER_SECRET"]
access_token = st.secrets["ACCESS_TOKEN"]
access_token_secret = st.secrets["ACCESS_TOKEN_SECRET"]


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


# Function to drop unnecessary columns and clean data
def clean_data(tweet_df):
    tweets_only_df = tweets_df.drop(columns=["user_id", "location"])

    # Remove http links from tweets
    def remove_http_https(text):
        return re.sub(r"http\S+", "", text)

    tweets_only_df["link_removed"] = tweets_only_df["tweet"].apply(
        lambda x: remove_http_https(x)
    )

    # remove @username from tweets
    def remove_username(text):
        return re.sub(r"@\S+", "", text)

    tweets_only_df["username_removed"] = tweets_only_df["link_removed"].apply(
        lambda x: remove_username(x)
    )

    # remove #hashtag from tweets
    def remove_hashtag(text):
        return re.sub(r"#\S+", "", text)

    tweets_only_df["hashtag_removed"] = tweets_only_df["username_removed"].apply(
        lambda x: remove_hashtag(x)
    )

    # Remove punctuations
    # string.punctuation
    def remove_punct(text):
        text = "".join([char for char in text if char not in string.punctuation])
        text = re.sub("[0-9]+", "", text)
        return text

    tweets_only_df["tweet_punct"] = tweets_only_df["hashtag_removed"].apply(
        lambda x: remove_punct(x)
    )

    # Tokenize the tweets
    def tokenize(text):
        text = re.split("\W+", text)
        return text

    tweets_only_df["tweet_tokenized"] = tweets_only_df["tweet_punct"].apply(
        lambda x: tokenize(x)
    )

    # Remove stopwords
    stopwords = nltk.corpus.stopwords.words("english")

    def remove_stopwords(text):
        text = [word for word in text if word not in stopwords]
        return text

    tweets_only_df["tweet_nonstop"] = tweets_only_df["tweet_tokenized"].apply(
        lambda x: remove_stopwords(x)
    )
    # Lemmatize the tweets

    ps = nltk.PorterStemmer()

    def stemming(text):
        text = [ps.stem(word) for word in text]
        return text

    tweets_only_df["tweet_stemmed"] = tweets_only_df["tweet_nonstop"].apply(
        lambda x: stemming(x)
    )

    wn = nltk.WordNetLemmatizer()

    def lemmatizer(text):
        text = [wn.lemmatize(word) for word in text]
        return text

    tweets_only_df["tweet_lemmatized"] = tweets_only_df["tweet_stemmed"].apply(
        lambda x: lemmatizer(x)
    )

    return tweets_only_df


# Function to create wordcloud of top 10 most used words
def word_cloud(df):
    all_final_tweets = " ".join(word for word in df["tweet_punct"])
    fig, ax = plt.subplots(figsize=(30, 30))
    wordcloud_all_tweets = WordCloud(
        max_font_size=50, max_words=50, background_color="black"
    ).generate(all_final_tweets)
    ax.imshow(wordcloud_all_tweets, interpolation="bilinear")
    ax.set_title(
        f"Word Cloud of Top 100 words",
        fontsize=20,
    )
    ax.axis("off")
    st.pyplot(fig)


# Functions to calculate subjectivity and polarity of tweets
def get_subjectivity(text):
    return TextBlob(text).sentiment.subjectivity


def get_polarity(text):
    return TextBlob(text).sentiment.polarity


# Compute negative, neutral, positive analysis of the tweets
def get_analysis(score):
    if score < 0:
        return "Negative"
    elif score == 0:
        return "Neutral"
    else:
        return "Positive"


def analyse_subjectivity(score):
    if score < 0.5:
        return "Objective"
    else:
        return "Subjective"


# Plot histogram of the polarity of the tweets
def plot_histogram(df):
    fig, ax = plt.subplots(figsize=(30, 30))
    ax = df["polarity"].hist(
        bins=20, color="blue", edgecolor="black", linewidth=1.2, figsize=(10, 6)
    )
    ax.set_title(f"Histogram of the Polarity of the Tweets", fontsize=12)
    ax.set_xlabel("Polarity", fontsize=12)
    ax.set_ylabel("Frequency", fontsize=12)
    st.pyplot(fig)


# Plot bar chart of the polarity of the tweets
def plot_bar_chart(df):
    fig, ax = plt.subplots(figsize=(30, 30))
    ax = (
        df["analysis"]
        .value_counts()
        .plot(
            kind="bar",
            color=["green", "blue", "red"],
            edgecolor="black",
            linewidth=1.2,
            figsize=(10, 6),
        )
    )
    ax.set_title(f"Bar Chart of the Polarity of the Tweets", fontsize=18)
    ax.set_xlabel("Polarity", fontsize=12)
    ax.set_ylabel("Frequency", fontsize=12)
    st.pyplot(fig)


# Plot pie chart of the polarity of the tweets
def plot_polarity_pie_chart(df):
    fig, ax = plt.subplots(figsize=(30, 30))
    ax = (
        df["analysis"]
        .value_counts()
        .plot(
            kind="pie",
            autopct="%1.1f%%",
            colors=["blue", "orange", "red"],
            figsize=(10, 6),
        )
    )
    ax.set_title(f"Pie Chart of the Polarity of the Tweets", fontsize=12)
    st.pyplot(fig)


# Plot pie chart of the subjectivity of the tweets
def plot_subjectivity_pie_chart(df):
    fig, ax = plt.subplots(figsize=(30, 30))
    ax = (
        df["subjectivity_analysis"]
        .value_counts()
        .plot(kind="pie", autopct="%1.1f%%", colors=["blue", "red"], figsize=(10, 6))
    )
    ax.set_title(f"Pie Chart of the Subjectivity of the Tweets", fontsize=12)
    st.pyplot(fig)


# Function to plot a scatter plot of the polarity and subjectivity of the tweets
def plot_scatter(df):
    fig = plt.figure(figsize=(30, 25))
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(
        df["polarity"],
        df["subjectivity"],
        color="blue",
        edgecolor="black",
        linewidth=1.2,
        s=50,
        marker="o",
        alpha=0.5,
    )
    ax.set_title(
        f"Scatter Plot of the Polarity and Subjectivity of the Tweets", fontsize=18
    )
    ax.set_xlabel("Polarity", fontsize=18)
    ax.set_ylabel("Subjectivity", fontsize=18)
    st.pyplot(fig)


def plot_analysis(df):
    clean_tweets_df = clean_data(tweets_df)
    word_cloud(clean_tweets_df)
    clean_tweets_df["subjectivity"] = clean_tweets_df["tweet"].apply(get_subjectivity)
    clean_tweets_df["polarity"] = clean_tweets_df["tweet"].apply(get_polarity)
    clean_tweets_df["analysis"] = clean_tweets_df["polarity"].apply(get_analysis)
    clean_tweets_df["subjectivity_analysis"] = clean_tweets_df["subjectivity"].apply(
        analyse_subjectivity
    )
    clean_tweets_df["analysis"].value_counts()
    plot_histogram(clean_tweets_df)
    plot_bar_chart(clean_tweets_df)
    plot_polarity_pie_chart(clean_tweets_df)
    plot_subjectivity_pie_chart(clean_tweets_df)
    plot_scatter(clean_tweets_df)


# Sidebar to choose to retrieve either Tweets by Username or Hashtag/Phrase
st.sidebar.title("Select the type of data you want to retrieve")
st.sidebar.subheader("Instructions:")
st.sidebar.markdown(
    """
    - Select the type of Tweets to retrieve.
    - For username, enter the username in the textbox without the @ symbol.
    - Enter hashtag(s) or phrase(s) to retrieve from Twitter
    - Separate multiple hashtags or phrases with OR or AND inside Double Quotes.
    - For example: "Python OR Machine Learning" or "Python AND Machine Learning"
    - Enter a number of tweets to retrieve (1 - 1000)
    - Click on the button to retrieve the Tweets & Run Analysis
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
        num_tweets = st.slider(
            "Select number of tweets to be retrieved:", 0, 1000, 100, 100
        )
        st.write(username)
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
            plot_analysis(tweets_df)

    else:
        keywords = st.text_input(
            "Enter the hashtag(s) or phrase(s) to retrieve from Twitter:"
        )
        num_tweets = st.slider(
            "Select number of tweets to be retrieved:", 0, 1000, 100, 100
        )
        keywords = list(set(keywords.split(",")))
        st.write(keywords)
        if st.button("Retrieve & Analyse Tweets"):
            tweets_df = get_tweets_by_search_term(keywords, num_tweets)

            st.markdown(
                """
        #### Summary of Tweets Retrieved
        """
            )
            st.write(tweets_df.shape[0], "tweets retrieved")
            st.write(tweets_df.shape[1], "columns retrieved")
            st.table(tweets_df.head())
            plot_analysis(tweets_df)
except BaseException as e:
    st.error(
        f"Something went wrong: Make sure you have entered a valid username or hashtag/phrase without any special characters : {e}"
    )
    pass
