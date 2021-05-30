import requests

ngrok_url = 'http://895390db25c9.ngrok.io'

tweets_endpoint = f'{ngrok_url}/usernametweets'
#search_endpoint = f'{ngrok_url}/searchtermtweets'

r_tweets = requests.post(tweets_endpoint, json={})
print(r_tweets.text)
#r_terms = requests.post(search_endpoint, json={})
#print(r_terms.text)