import webapp2
import cgi
import jinja2
import os
import models
import time
import fanhype
import json
from google.appengine.ext import ndb


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class NewGame(webapp2.RequestHandler):

    def get(self):

    	games = models.HypeTable.query().fetch()
    	template_values = {'games': games}

        template = JINJA_ENVIRONMENT.get_template('new_game.html')
        self.response.write(template.render(template_values))

    def post(self):

		password = cgi.escape(self.request.get('password'))
		if password != "nahdude":
			self.redirect("/newgame")
			return;

		teamOneName = cgi.escape(self.request.get('teamOneName'))
		teamTwoName = cgi.escape(self.request.get('teamTwoName'))
		hypeTable = models.HypeTable()
		hypeTable.teamOneName = teamOneName
		hypeTable.teamTwoName = teamTwoName
		hypeTable.teamOneHashTags = cgi.escape(self.request.get('teamOneHashtags'))
		hypeTable.teamTwoHashTags = cgi.escape(self.request.get('teamTwoHashtags'))
		hypeTable.teamOneColor = cgi.escape(self.request.get('teamOneColor'))
		hypeTable.teamTwoColor = cgi.escape(self.request.get('teamTwoColor'))
		hypeTable.teamOneImage = cgi.escape(self.request.get('teamOneImage'))
		hypeTable.teamTwoImage = cgi.escape(self.request.get('teamTwoImage'))
		hypeTable.gameTitle = cgi.escape(self.request.get('gameTitle'))
		hypeTable.gameTime = cgi.escape(self.request.get('gameTime'))
		hypeTable.gameLocation = cgi.escape(self.request.get('gameLocation'))
		hypeTable.teamOneHype = 0
		hypeTable.teamTwoHype = 0
		hypeTable.teamOneTweetTotal = 0
		hypeTable.teamTwoTweetTotal = 0
		hypeTable.put()

		geoData = models.GeoData()
		geoData.coordinates = ""
		geoData.teamName = teamOneName
		geoData.put()

		geoData = models.GeoData()
		geoData.coordinates = ""
		geoData.teamName = teamTwoName
		geoData.put()

		time.sleep(1)
		self.redirect("/newgame")

class ClearGameData(webapp2.RequestHandler):
	def post(self):

		password = cgi.escape(self.request.get('password'))
		if password != "nahdude":
			self.redirect("/newgame")
			return;

		team_one_name = self.request.get('one')
		team_two_name = self.request.get('two')
		hypeTable = models.HypeTable.query(ndb.OR(models.HypeTable.teamOneName == team_one_name, models.HypeTable.teamOneName == team_two_name)).fetch()
		for row in hypeTable:
			row.teamOneHype = 0
			row.teamTwoHype = 0
			row.teamOneTweetTotal = 0
			row.teamTwoTweetTotal = 0
			row.put()

		coordinates = models.GeoData.query(ndb.OR(models.GeoData.teamName == team_one_name, models.GeoData.teamName == team_two_name)).fetch()
		for row in coordinates:
			row.coordinates = ""
			row.put()

		topTweets = models.TopTweet.query(ndb.OR(models.GeoData.teamName == team_one_name, models.GeoData.teamName == team_two_name)).fetch()
		[row.key.delete() for row in topTweets]	


		latestTweets = models.LatestTweets.query(ndb.OR(models.LatestTweets.teamName == team_one_name, models.LatestTweets.teamName == team_two_name)).fetch()
		[row.key.delete() for row in latestTweets]	
		
		time.sleep(1)
		self.redirect("/newgame")

class DeleteGame(webapp2.RequestHandler):
	def post(self):

		password = cgi.escape(self.request.get('password'))
		if password != "nahdude":
			self.redirect("/newgame")
			return;

		team_one_name = self.request.get('one')
		team_two_name = self.request.get('two')
		hypeTable = models.HypeTable.query(ndb.OR(models.HypeTable.teamOneName == team_one_name, models.HypeTable.teamOneName == team_two_name)).fetch()
		[row.key.delete() for row in hypeTable]

		coordinates = models.GeoData.query(ndb.OR(models.GeoData.teamName == team_one_name, models.GeoData.teamName == team_two_name)).fetch()
		[row.key.delete() for row in coordinates]

		topTweets = models.TopTweet.query(ndb.OR(models.GeoData.teamName == team_one_name, models.GeoData.teamName == team_two_name)).fetch()
		[row.key.delete() for row in topTweets]
		
		time.sleep(1)
		self.redirect("/newgame")

class Import(webapp2.RequestHandler):
	def post(self):

		password = cgi.escape(self.request.get('password'))
		if password != "nahdude":
			self.redirect("/newgame")
			return;
		
		tweets_json = cgi.escape(self.request.get('tweets'))
		tweet_string = str(tweets_json).split("\n")

		tweets = []
		for line in tweet_string:
			try:
				tweets.append (json.loads (line.strip()))
			except:
				print "Error decoding JSON: " + str(line)

		fanhype.saveNewTweets (tweets)
		time.sleep(1)
		self.redirect("/newgame")
