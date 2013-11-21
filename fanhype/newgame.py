import webapp2
import cgi
import jinja2
import os
import models


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class NewGame(webapp2.RequestHandler):

    def get(self):
    	template_values = {'name': 'Jason!'}
        template = JINJA_ENVIRONMENT.get_template('new_game.html')
        self.response.write(template.render(template_values))

    def post(self):
        hypeTable = models.HypeTable()
        hypeTable.teamOneName = cgi.escape(self.request.get('teamOneName'))
        hypeTable.teamTwoName = cgi.escape(self.request.get('teamTwoName'))
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

        self.response.write('Created a new hypeTable entry!')
