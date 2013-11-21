import webapp2
import cgi
import jinja2
import os
import models
import time
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

class DeleteGame(webapp2.RequestHandler):
	def post(self):
		team_one_name = self.request.get('one')
		team_two_name = self.request.get('two')
		hypeTable = models.HypeTable.query(ndb.OR(models.HypeTable.teamOneName == team_one_name, models.HypeTable.teamOneName == team_two_name)).fetch()
		[row.key.delete() for row in hypeTable]

		coordinates = models.GeoData.query(ndb.OR(models.GeoData.teamName == team_one_name, models.GeoData.teamName == team_two_name)).fetch()
		[row.key.delete() for row in coordinates]
		
		time.sleep(1)
		self.redirect("/newgame")






