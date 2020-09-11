import requests, json

r = requests.get('https://covidtracking.com/api/states/daily')

x = json.loads(r.text)


