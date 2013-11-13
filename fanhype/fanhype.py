import webapp2
import cgi
from google.appengine.ext import ndb
import jinja2
import os
from query_tweet_collector import TweetCollector
from models import ApplicationData
import tweepy
from tweepy import OAuthHandler
import config


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Tweet(ndb.Model):
	screen_name = ndb.StringProperty(indexed=False)
	image_url = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)

class MainPage(webapp2.RequestHandler):
        def get(self):                
                template = JINJA_ENVIRONMENT.get_template('index.html')
                self.response.write(template.render(title = "Howdy"))

class SingleGame(webapp2.RequestHandler):
    def post(self):
        collector = TweetCollector()
        query = "Kentucky"
        listOfTweets = []
        #listOfTweets = collector.CollectTweets(query)
        collector.CollectTweets(query)

        #appDataQuery = ApplicationData.query()
        #tweets = appDataQuery.fetch(5)
        tweets = ApplicationData.queryTweets()
        for tweet in tweets:
                listOfTweets.append(tweet.tweetText)
        #collector.CollectTweets(query)
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
                query = "Obama"
                tw = {}
                        
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
                    imageURL = tweet.user.profile_image_url_https       #.encode('utf-8')
                    #printList.append((imageURL,tweetText))
                    printList.append(tweetText)

                appData = ApplicationData()
                appData.tweetText = tweetText
                appData.put()   

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/gamehype', SingleGame),
    ('/cron', TweetScript),
], debug=True)
