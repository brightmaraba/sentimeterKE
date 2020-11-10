import requests

ngrok_url = ' https://739a47a90d87.ngrok.io'

endpoint = f'{ngrok_url}/usernametweets'

r = requests.get(endpoint, json={})
print(r.text)