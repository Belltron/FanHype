import tweepy
from twython import Twython
import config

c = config.Config()
keys = c.get_keys()

consumer_key = keys[0]
consumer_secret = keys[1]
access_token_key = keys[2]
access_token_secret = keys[3]

twitter = Twython(consumer_key, consumer_secret,
                  access_token_key, access_token_secret)

tweets =  twitter.search(q='kanye',geodata='36.50,20.43,10mi')
for tweet in tweets['statuses']:
	print tweet['text']

print '------------------------'
print '         twython'
print '         ........'
print '         tweepy'
print '------------------------'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)

api = tweepy.API(auth)

tweets = api.search(q='kanye',
        count=20,
        result_type='recent',
        geodata='36.50,20.43,10mi',
        lang='en')

for tweet in tweets:
	print tweet.text.encode('utf-8')