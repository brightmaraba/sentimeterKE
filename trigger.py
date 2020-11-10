import requests

ngrok_url = ' https://739a47a90d87.ngrok.io'

endpoint_1 = f'{ngrok_url}/usernametweets'
endpoint_2 = f'{ngrok_url}/searchtermtweets'

r = requests.get(endpoint_1, json={})
print(r.text)
r = requests.get(endpoint_2, json={})
print(r.text)