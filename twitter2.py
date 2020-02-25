import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl

# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def twit(user):
    while True:
            acct = user
            if len(acct) < 1:
                break
            url = twurl.augment(TWITTER_URL,
                                {'screen_name': acct, 'count': '100'})
            print('Retrieving', url)
            connection = urllib.request.urlopen(url, context=ctx)
            data = connection.read().decode()
            js = json.loads(data)
            with open('twit.json', 'w') as f:
                json.dump(js, f,  ensure_ascii=False, indent=4)
                y = json.dumps(js, indent = 2)
            return js
