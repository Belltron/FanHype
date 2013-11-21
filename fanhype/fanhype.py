import webapp2
import cgi
import jinja2
import os
import random
import json
from google.appengine.ext import ndb, db
import jinja2
import os
from query_tweet_collector import TweetCollector
from models import ApplicationData, Tweet, HypeTable, GeoData
import tweepy
from tweepy import OAuthHandler
import config
#from analyzer import GameHype
import analyzer


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
        def get(self):
            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render())
            """
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
                """

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

class Game(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('game.html')

        tweets_query = ndb.gql('SELECT * FROM Tweet WHERE latitude != null')
        tweets = tweets_query.fetch()

        #Example separation of tweets into two teams' tweets.
        team_one_tweets = [tweet for tweet in tweets if  tweet.latitude > 40]
        team_two_tweets = [tweet for tweet in tweets if  tweet.latitude < 40]

        team_one_tags = ['everyoneinblack', 'sicou', 'baylor', 'sicem', 'sicembears']
        team_two_tags = ['oklahoma','boomersooner', 'gosooners', 'beatbaylor']
        game_tweets_query = ndb.gql('SELECT * FROM Tweet')
        tweets = game_tweets_query.fetch()
        
        hypeTuple = analyzer.calculateHype(tweets, team_one_tags, team_two_tags)
        
        baylorTotal = hypeTuple[0]
        baylorHype = hypeTuple[1]    
    
        oklahomaTotal = hypeTuple[2]
        oklahomaHype = hypeTuple[3]
        template_values = {
            'baylor_total': baylorTotal,
            'baylor_hype': baylorHype,
            'oklahoma_total': oklahomaTotal,
            'oklahoma_hype': oklahomaHype,
            'team_one_tweets': team_one_tweets,
            'team_two_tweets': team_two_tweets
        }
        self.response.write(template.render(template_values))

class SaveTweet(webapp2.RequestHandler):
    def get(self):
        lat = -83.74886513
        lon = 42.26584491
        lat += random.randint(0,4) - 2
        lon += random.randint(0,4) - 2                                                                                       
        new_tweet = Tweet()
        new_tweet.screen_name = 'Tweet'
        new_tweet.coordinates = ndb.GeoPt(lat, lon)
        new_tweet.hashTags = "beatbaylor"
        new_tweet.put()
        self.response.write('Added data point at: ('+str(lat)+', '+str(lon)+')')

    def post(self):

        tweets = json.loads(self.request.body)
        hypeTables = HypeTable.query().fetch()

        newTweetsTeamOne = []
        newTweetsTeamTwo = []

        for tweet in tweets:
            for hypeTable in hypeTables:
                for hashtag in tweet['entities']['hashtags']:
                    if hashtag['text'] in hypeTable.teamOneHashTags:
                        hypeScore = analyzer.calculateHype([tweet], hypeTable.teamOneHashTags, HypeTable.teamTwoHashTags)
                        #print "Hype Score: " + str(hypeScore[1])
                    if hashtag['text'] in hypeTable.teamTwoHashTags:
                        hypeScore = analyzer.calculateHype([tweet], hypeTable.teamTwoHashTags, HypeTable.teamOneHashTags)
                        #print "Hype Score: " + str(hypeScore[1])

        

        #q = GeoData.query(GeoData.teamName == 'Oklahoma')
        #print str(q.fetch())
        



application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/gamehype', SingleGame),
    ('/cron', TweetScript),
    ('/game', Game),
    ('/savetweet', SaveTweet),
], debug=True)
