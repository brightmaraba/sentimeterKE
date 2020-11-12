import requests

ngrok_url = 'http://f68159668a31.ngrok.io'

tweets_endpoint = f'{ngrok_url}/usernametweets'
search_endpoint = f'{ngrok_url}/searchtermtweets'

r_tweets = requests.get(tweets_endpoint, json={})
print(r_tweets.text)
r_terms = requests.get(search_endpoint, json={})
print(r_terms.text)