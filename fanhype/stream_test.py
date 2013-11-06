import json
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from twython import Twython
import config


class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    def on_data(self, data):
        tweet = json.loads(data)
        print tweet['text']
        return True

    def on_error(self, status):
        print status

c = config.Config()
keys = c.get_keys()

auth = OAuthHandler(keys[0], keys[1])
auth.set_access_token(keys[2], keys[3])

l = StdOutListener()

stream = Stream(auth, l)
stream.filter(track=['kanye'])