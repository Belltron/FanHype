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
import time
import logging


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

        team_one_top_list = models.TopTweet.query(team_one_name == models.TopTweet.teamName).fetch()
        team_two_top_list = models.TopTweet.query(team_two_name == models.TopTweet.teamName).fetch()

        team_one_top = team_one_top_list[0] if len(team_one_top_list) > 0 else {}
        team_two_top = team_two_top_list[0] if len(team_two_top_list) > 0 else {}

        latest_tweets = []

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
            'team_two_top': team_two_top,
            'latest_tweets': latest_tweets
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

        saveNewTweets(tweets)

def saveNewTweets(tweets):
    hypeTables = models.HypeTable.query().fetch()
    geoData = models.GeoData.query().fetch()

    #This code used for resetting all values
    """for row in geoData:
        row.coordinates = ""
    for row in hypeTables:
        row.teamOneHype = 0
        row.teamTwoHype = 0
        row.teamOneTweetTotal = 0
        row.teamTwoTweetTotal = 0"""
        
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

    [row.put() for row in geoData]
    [row.put() for row in hypeTables]

def addTweetCoordinates(tweet, geoData, teamName):
    if 'coordinates' in tweet and tweet['coordinates']:
        coordinates = tweet['coordinates']['coordinates']
        for data in geoData:
            if data.teamName == teamName:
                data.coordinates += str(coordinates[0]) + "," + str(coordinates[1]) + "|"
                
def getLatestTweets(tweets):
    team = ""
    if len(tweets) >= 5:
        lastFiveTweets = tweets[-5:]
    else:
        tweetsLength = len(tweets)
        lastFiveTweets = tweets[-tweetsLength:]  
    team = (lastFiveTweets[-1])['teamname']
            
    dataStoreLatestTweets = models.LatestTweets.query(models.TopTweet.teamName == team).fetch()
    tempTweets = dataStoreLatestTweets
    [row.key.delete() for row in tempTweets]   
    
    latestTweets = []
    for lTweet in lastFiveTweets:
        latestTweet = models.LatestTweets()
        if 'teamname' in lTweet:
            latestTweet.teamName = lTweet['teamname']
        latestTweet.imageUrl = lTweet['user']['profile_img_url']
        latestTweet.tweetText = lTweet['text']
        latestTweet.userName = lTweet['user']['screen_name']
        if 'hypescore' in lTweet:
            latestTweet.hypeScore = str(lTweet['hypescore'])
        latestTweet.createdAt = lTweet['created_at']
        logging.info(lTweet['created_at'])
        latestTweet.followerCount = str(lTweet['user']['followers_count'])
        add = True
        if len(dataStoreLatestTweets) > 0:
            for dslt in dataStoreLatestTweets:
                if latestTweet.userName == dslt.userName:
                    add = False
            if add:
                latestTweets.append(latestTweet)
        else: latestTweets.append(latestTweet)
    if len(dataStoreLatestTweets) == 0:
        for dst in latestTweets:
            dst.put()
    else:
        dataStoreLatestTweets += latestTweets
        putLatest = sorted(dataStoreLatestTweets, key = lambda t : time.strptime(t.createdAt, "%a %b %d %H:%M:%S +0000 %Y"))
        for dst in putLatest[-5:]:
            dst.put()    

def calculateTopTweet(tweets):
    if tweets:
        top_tweet = max(tweets, key=lambda x:x['hypescore'])
        if top_tweet:
            topTweet = models.TopTweet.query(models.TopTweet.teamName == top_tweet['teamname']).fetch();
            
            if len(topTweet) == 0:
                topTweet = models.TopTweet()
            else:
                topTweet = topTweet[0]
                if float(topTweet.hypeScore) >= float(top_tweet['hypescore']):
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
    ('/game', Game),
    ('/savetweet', SaveTweet),
    ('/newgame', game_control.NewGame),
    ('/deletegame', game_control.DeleteGame),
    ('/import', game_control.Import),
    ('/cleargame', game_control.ClearGameData)
], debug=True)
