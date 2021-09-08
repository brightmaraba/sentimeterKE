from fastapi import FastAPI
import get_tweets
from logger import trigger_log_tweets
from logger import trigger_log_search

app = FastAPI()

@app.post("/usernametweets")
def get_tweets_per_username():
    trigger_log_tweets()
    get_tweets.get_tweets_by_username("LibranTechie", 1000)
    return {"Message": "Done"}

@app.post("/searchtermtweets")
def get_tweets_by_searchterm():
    trigger_log_search()
    get_tweets.get_tweets_by_search_term(['Laikipia'])
    return {"Message": "Done"}