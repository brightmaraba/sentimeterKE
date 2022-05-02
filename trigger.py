import requests

ngrok_url = "https://a262-49-196-234-22.au.ngrok.io "

tweets_endpoint = f"{ngrok_url}/usernametweets"
search_endpoint = f"{ngrok_url}/searchtermtweets"

r_tweets = requests.post(tweets_endpoint, json={})
print(r_tweets.text)
r_terms = requests.post(search_endpoint, json={})
print(r_terms.text)
