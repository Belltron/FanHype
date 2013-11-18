import webapp2
import cgi
from google.appengine.ext import ndb
import jinja2
import os
from query_tweet_collector import TweetCollector
from models import ApplicationData, Tweet
import tweepy
from tweepy import OAuthHandler
import config


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
        def get(self):                
                template = JINJA_ENVIRONMENT.get_template('index.html')
                self.response.write(template.render(title = "Howdy"))

                new_tweet = Tweet()
                new_tweet.tweetText = "test"
                new_tweet.hashTags = ['lol', 'yup', 'aggies']
                new_tweet.coordinates = ndb.GeoPt(-36.654, 26.546)
                new_tweet.put()


class SingleGame(webapp2.RequestHandler):
    def post(self):
        collector = TweetCollector()
        query = "Kentucky"
        listOfTweets = []
        #collector.CollectTweets(query)
        tweets = ApplicationData.queryTweets().fetch(5)
        for tweet in tweets:
                listOfTweets.append(tweet.tweetText)
        template_values = {'listOfTweets': listOfTweets,}
                
        template = JINJA_ENVIRONMENT.get_template('gamehype.html')
        self.response.write(template.render(template_values))

class TweetScript(webapp2.RequestHandler):
        def get(self):                        
                c = config.Config()
                keys = c.get_keys()
                auth = OAuthHandler(keys[0], keys[1])
                auth.set_access_token(keys[2], keys[3])        
                api = tweepy.API(auth)
                query = "Johnny Football"
                tw = {}
                #appData = ApplicationData()
                        
                tweetList = []
                tweetText = ""
                hashTags = []
                tagInfo = []
                tagTuples = []
                printList = []
                for tweet in tweepy.Cursor(api.search,
                    q=query,
                    rpp=100,
                    result_type="recent",
                    include_entities=True,
                    lang="en").items(5):
                    tweetText = tweet.text      #.encode('utf-8')
                    appData = ApplicationData()
                    appData.tweetText = tweetText
                    appData.put()

                #appData = ApplicationData()
                #appData.tweetText = tweetText
                #appData.put()   

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/gamehype', SingleGame),
    ('/cron', TweetScript),
], debug=True)
