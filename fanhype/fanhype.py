import webapp2
import jinja2
import os
import random
from google.appengine.ext import ndb


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname('__file__')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class Tweet(ndb.Model):
	screen_name = ndb.StringProperty(indexed=False)
	coordinates = ndb.GeoPtProperty()
	date = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('html/index.html')

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

class SaveTweet(webapp2.RequestHandler):
    def get(self):
        lat = 39.8282
        lon = -98.5795
        new_tweet = Tweet()
        new_tweet.screen_name = 'Tweet'
        new_tweet.coordinates = ndb.GeoPt(lat, lon)
        new_tweet.put()
        self.response.write('Added data point at: ('+str(lat)+', '+str(lon)+')')


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/savetweet', SaveTweet),
], debug=True)
