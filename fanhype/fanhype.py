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
import models
import tweepy
from tweepy import OAuthHandler
import config
import analyzer
import game_control


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')

        games = models.HypeTable.query().fetch()
        template_values = {'games': games}
        self.response.write(template.render(template_values))



class SingleGame(webapp2.RequestHandler):
    def post(self):
        collector = TweetCollector()
        query = "Kentucky"
        listOfTweets = []
        #collector.CollectTweets(query)
        tweets = models.ApplicationData.queryTweets().fetch(5)
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
            appData = models.ApplicationData()
            appData.tweetText = tweetText
            appData.put()   

class Game(webapp2.RequestHandler):
    def get(self):

        template = JINJA_ENVIRONMENT.get_template('game.html')

        team_one_name = self.request.get('one')
        team_two_name = self.request.get('two')

        hypeTable = models.HypeTable.query(ndb.OR(models.HypeTable.teamOneName == team_one_name, models.HypeTable.teamOneName == team_two_name)).fetch()[0]

        team_one_coordinates = models.GeoData.query(models.GeoData.teamName == hypeTable.teamOneName).fetch()[0].coordinates.split('|')
        team_two_coordinates = models.GeoData.query(models.GeoData.teamName == hypeTable.teamTwoName).fetch()[0].coordinates.split('|')

        team_one_points = [models.Point(point) for point in team_one_coordinates]
        team_two_points = [models.Point(point) for point in team_two_coordinates]

        team_one_top = models.TopTweet.query(team_one_name == models.TopTweet.teamName).fetch()[0]
        team_two_top = models.TopTweet.query(team_two_name == models.TopTweet.teamName).fetch()[0]

        template_values = {
            'game_title': hypeTable.gameTitle,
            'game_time': hypeTable.gameTime,
            'game_location': hypeTable.gameLocation,
            'team_one_color': hypeTable.teamOneColor,
            'team_two_color': hypeTable.teamTwoColor,
            'team_one_name': hypeTable.teamOneName,
            'team_two_name': hypeTable.teamTwoName,
            'team_one_total': hypeTable.teamOneTweetTotal,
            'team_two_total': hypeTable.teamTwoTweetTotal,
            'team_one_hype': hypeTable.teamOneHype,
            'team_two_hype': hypeTable.teamTwoHype,
            'team_one_image': hypeTable.teamOneImage,
            'team_two_image': hypeTable.teamTwoImage,
            'team_one_hashtags': hypeTable.teamOneHashTags.split(','),
            'team_two_hashtags': hypeTable.teamTwoHashTags.split(','),
            'team_one_tweets': team_one_points,
            'team_two_tweets': team_two_points,
            'team_one_top': team_one_top,
            'team_two_top': team_two_top
        }
        self.response.write(template.render(template_values))


class SaveTweet(webapp2.RequestHandler):
    def get(self):
        models.initializeModels()
        print "Initialized models"

    def post(self):        
        tweets = json.loads(self.request.body)
        if len(tweets) == 0:
            return;
        hypeTables = models.HypeTable.query().fetch()
        geoData = models.GeoData.query().fetch()
        # get 5 most recent tweets

        #This code used for resetting all values
        for row in geoData:
            row.coordinates = ""

        for row in hypeTables:
            row.teamOneHype = 0
            row.teamTwoHype = 0
            row.teamOneTweetTotal = 0
            row.teamTwoTweetTotal = 0

        for tweet in tweets:
            tweet['hypescore'] = 0
            tweet['teamname'] = ""

        for hypeTable in hypeTables:
            team_one_tags = hypeTable.teamOneHashTags.split(',')
            team_two_tags = hypeTable.teamTwoHashTags.split(',')
            for tweet in tweets:
                for hashtag in tweet['entities']['hashtags']:
                    hypeScore = analyzer.calculateHypeJson([tweet], team_one_tags, team_two_tags)
                    if hashtag['text'].lower() in team_one_tags:
                        hypeTable.teamOneHype += hypeScore[0]
                        hypeTable.teamOneTweetTotal += 1                       
                        tweet['hypescore'] = hypeScore[0]
                        tweet['teamname'] = hypeTable.teamOneName
                        addTweetCoordinates(tweet, geoData, hypeTable.teamOneName)
                    elif hashtag['text'].lower() in team_two_tags:
                        hypeTable.teamTwoHype += hypeScore[1]
                        tweet['hypescore'] = hypeScore[1]
                        tweet['teamname'] = hypeTable.teamTwoName
                        hypeTable.teamTwoTweetTotal += 1
                        addTweetCoordinates(tweet, geoData, hypeTable.teamTwoName)

        #Find the top tweet of the new tweets
        for hypeTable in hypeTables:
            team_one_game_tweets = [tweet for tweet in tweets if tweet['teamname'] == hypeTable.teamOneName]
            calculateTopTweet(team_one_game_tweets)
            team_two_game_tweets = [tweet for tweet in tweets if tweet['teamname'] == hypeTable.teamTwoName]
            calculateTopTweet(team_two_game_tweets)

        [row.put() for row in geoData];
        [row.put() for row in hypeTables];

def addTweetCoordinates(tweet, geoData, teamName):
    if 'coordinates' in tweet and tweet['coordinates']:
        coordinates = tweet['coordinates']['coordinates']
        for data in geoData:
            if data.teamName == teamName:
                data.coordinates += str(coordinates[0]) + "," + str(coordinates[1]) + "|"

def calculateTopTweet(tweets):
    if tweets:
        top_tweet = tweets[0]
        
        for tweet in tweets:
            if 'hypescore' in tweet and tweet['hypescore'] > top_tweet['hypescore']:
                top_tweet = tweet
        print "top tweet score: " + str(top_tweet['hypescore'])
        topTweet = models.TopTweet.query(models.TopTweet.teamName == top_tweet['teamname']).fetch();
        if len(topTweet) == 0:
            topTweet = models.TopTweet()
        else:
            topTweet = topTweet[0]
            if float(topTweet.hypeScore) >= float(top_tweet['hypescore']):
                print "current top: " + str(topTweet.hypeScore) + " new: " + str(top_tweet['hypescore']) + " team: "+str(top_tweet['teamname'])
                return
        
        topTweet.teamName = top_tweet['teamname']
        topTweet.imageUrl = top_tweet['user']['profile_img_url']
        topTweet.tweetText = top_tweet['text']
        topTweet.userName = top_tweet['user']['screen_name']
        topTweet.hypeScore = str(top_tweet['hypescore'])
        topTweet.followerCount = str(top_tweet['user']['followers_count'])
        topTweet.createdAt = top_tweet['created_at']
        topTweet.put()



application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/gamehype', SingleGame),
    ('/cron', TweetScript),
    ('/game', Game),
    ('/savetweet', SaveTweet),
    ('/newgame', game_control.NewGame),
    ('/deletegame', game_control.DeleteGame)
], debug=True)
