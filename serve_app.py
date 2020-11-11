
from fastapi import FastAPI
import get_tweets

app = FastAPI()

@app.post("/usernametweets")
def get_tweets_per_username():
    get_tweets.get_tweets_by_username("LibranTechie", 50)
    return {"Message": "Done"}

@app.post("/searchtermtweets")
def get_tweets_by_searchterm():
    get_tweets.get_tweets_by_search_term(['RejectBBI'])
    return {"Message": "Done"}
