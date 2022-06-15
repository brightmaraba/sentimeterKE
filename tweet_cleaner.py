import re
import string
import nltk

# Import NLTK Lexicon
# Import NLTK lexicon
nltk.download("vader_lexicon")
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("omw-1.4")

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
