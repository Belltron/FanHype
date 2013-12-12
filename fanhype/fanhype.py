import webapp2
import cgi
import jinja2
import os
import random
import json
from google.appengine.ext import ndb, db
import jinja2
import os
import models
import config
import analyzer
import game_control
import time
from datetime import datetime
import logging
from email.utils import parsedate
from pytz import timezone
import math

tweet_time_format = "%a %b %d %H:%M:%S +0000 %Y"
central = timezone('US/Central')
utc = timezone('UTC')


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

class About(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('about.html')
        self.response.write(template.render())

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

        latest_tweets = models.LatestTweets.query(ndb.OR(models.LatestTweets.teamName == team_one_name, models.LatestTweets.teamName == team_two_name)).fetch()
        random.shuffle(latest_tweets)

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
            'latest_tweets': latest_tweets,
            'hype_history': hypeTable.gameHypeHistory,
            'time_history': hypeTable.gameTimeHistory
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

def get_date_time(time_str):
    date_time = datetime.strptime(time_str, tweet_time_format)
    date_time = utc.localize(date_time)
    return central.normalize(date_time.astimezone(central))

def time_string(date_time):
    return str(date_time.hour) + ":" + str(date_time.minute)

        
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

    if tweets:
        current_time = get_date_time(tweets[0]['created_at'])
        history_time_string = ""
        history_hype_string = ""
        history_hype_one = 0
        history_hype_two = 0
    
    for tweet in tweets:
        tweet_time = get_date_time(tweet['created_at'])
        if (tweet_time - current_time).total_seconds() > 300:
            current_time = tweet_time
            history_time_string += time_string(tweet_time) + ','
            delta_hype = 0
            if history_hype_one + history_hype_two != 0:
                delta_hype = history_hype_one/(history_hype_one + history_hype_two) * 100
            history_hype_string += str(int(delta_hype)) + ","
            history_hype_one = 0
            history_hype_two = 0

        for hypeTable in hypeTables:
            team_one_tags = [tag.lower() for tag in hypeTable.teamOneHashTags.split(',')]
            team_two_tags = [tag.lower() for tag in hypeTable.teamTwoHashTags.split(',')]
            hypeScore = analyzer.calculateHypeJson(tweet, team_one_tags, team_two_tags)
            hs1 = math.fabs(hypeScore[0])
            hs2 = math.fabs(hypeScore[1])

            isTeamOne = False
            isTeamTwo = False
            for hashtag in tweet['entities']['hashtags']:
                if hashtag['text'].lower() in team_one_tags:
                    isTeamOne = True
                if hashtag['text'].lower() in team_two_tags:
                    isTeamTwo = True

            if isTeamOne and not isTeamTwo:
                tweet['hypescore'] = hs1
                tweet['teamname'] = hypeTable.teamOneName
                history_hype_one += hs1
                hypeTable.teamOneHype += hs1
                hypeTable.teamOneTweetTotal += 1
                addTweetCoordinates(tweet, geoData, hypeTable.teamOneName)
            if isTeamTwo and not isTeamOne:
                tweet['hypescore'] = hs2
                tweet['teamname'] = hypeTable.teamTwoName
                history_hype_two += hs2
                hypeTable.teamTwoHype += hs2
                hypeTable.teamTwoTweetTotal += 1
                addTweetCoordinates(tweet, geoData, hypeTable.teamTwoName)

    #Find the top tweet of the new tweets
    for hypeTable in hypeTables:
        team_one_game_tweets = [tweet for tweet in tweets if tweet['teamname'] == hypeTable.teamOneName]
        if len(team_one_game_tweets) > 200:
            hypeTable.gameHypeHistory += history_hype_string
            hypeTable.gameTimeHistory += history_time_string
        calculateTopTweet(team_one_game_tweets)
        getLatestTweets(team_one_game_tweets, hypeTable.teamOneName)
        team_two_game_tweets = [tweet for tweet in tweets if tweet['teamname'] == hypeTable.teamTwoName]
        calculateTopTweet(team_two_game_tweets)
        getLatestTweets(team_two_game_tweets, hypeTable.teamTwoName)

    [row.put() for row in geoData]
    [row.put() for row in hypeTables]

def addTweetCoordinates(tweet, geoData, teamName):
    if 'coordinates' in tweet and tweet['coordinates']:
        coordinates = tweet['coordinates']['coordinates']
        for data in geoData:
            if data.teamName == teamName:
                data.coordinates += str(coordinates[0]) + "," + str(coordinates[1]) + "|"
                
def getLatestTweets(tweets, teamName):

    team = ""
    if len(tweets) >= 5:
        lastFiveTweets = tweets[-5:]
    else:
        tweetsLength = len(tweets)
        lastFiveTweets = tweets[-tweetsLength:] 
    team = teamName
            
    dataStoreLatestTweets = models.LatestTweets.query(models.TopTweet.teamName == teamName).fetch()
    tempTweets = dataStoreLatestTweets
    [row.key.delete() for row in tempTweets]   
    
    latestTweets = []
    for lTweet in lastFiveTweets:
        latestTweet = models.LatestTweets()
        if 'teamname' in lTweet:
            latestTweet.teamName = lTweet['teamname']
        latestTweet.imageUrl = lTweet['user']['profile_image_url']
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
        putLatest = sorted(dataStoreLatestTweets, key = lambda t : time.strptime(t.createdAt, tweet_time_format))
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
            topTweet.imageUrl = top_tweet['user']['profile_image_url']
            topTweet.tweetText = top_tweet['text']
            topTweet.userName = top_tweet['user']['screen_name']
            topTweet.hypeScore = str(top_tweet['hypescore'])
            topTweet.followerCount = str(top_tweet['user']['followers_count'])
            topTweet.createdAt = top_tweet['created_at']
            topTweet.put()



application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/about', About),
    ('/game', Game),
    ('/savetweet', SaveTweet),
    ('/newgame', game_control.NewGame),
    ('/deletegame', game_control.DeleteGame),
    ('/import', game_control.Import),
    ('/cleargame', game_control.ClearGameData)
], debug=True)
