import requests
r = requests.get('https://www.reddit.com/r/wallstreetbets.json', headers = {'User-agent': 'dagster-bot 0.1'})
print(r.text)