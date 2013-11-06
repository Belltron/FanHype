import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Go to http://dev.twitter.com and create an app.
# twitter api stuff
consumer_key = 'XX0FySS0uEsbyLouAz6TrA'
consumer_secret = 'mfVitlnsTZbNIPQlPbqj5cJeQonVZnUepXBPppnai0'
access_token = '1360662272-bogDckLPDIldQIWnIMQpOohP5mb4v3wcqLu5CO0'
access_token_secret = 'hPdpoFkpaykuUcSidGBeDdnv6qbQv3x6BTXECigJTo'

class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    def on_data(self, data):
        tweet = json.loads(data)
        print tweet
        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=['#gostanford'])