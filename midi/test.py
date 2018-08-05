import requests


data = requests.get('http://smurakami.com:8888/data/timestamp.json').json()
print(data['timestamp'])
