import webapp2
import cgi
import jinja2
import os
import random
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
            
            tweet_query = Tweet.query()
            tweets = tweet_query.fetch()

            #Example separation of tweets into two teams' tweets.
            team_one_tweets = [tweet for tweet in tweets if tweet.coordinates.lat > 40]
            team_two_tweets = [tweet for tweet in tweets if tweet.coordinates.lat < 40]

            template_values = {
                'team_one_tweets': team_one_tweets,
                'team_two_tweets': team_two_tweets
            }
            self.response.write(template.render(template_values))


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

class SaveTweet(webapp2.RequestHandler):
    def get(self):
        lat = 39.8282
        lon = -98.5795
        new_tweet = Tweet()
        new_tweet.screen_name = 'Tweet'
        new_tweet.coordinates = ndb.GeoPt(lat, lon)
        new_tweet.put()
        self.response.write('Added data point at: ('+str(lat)+', '+str(lon)+')')

                #appData = ApplicationData()
                #appData.tweetText = tweetText
                #appData.put()   

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/gamehype', SingleGame),
    ('/cron', TweetScript),
    ('/savetweet', SaveTweet),
], debug=True)
