import webapp2
import cgi
from google.appengine.ext import ndb
import jinja2
import os
from query_tweet_collector import TweetCollector


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
        query = "Nebraska"
        listOfTweets = collector.CollectTweets(query)

        template_values = {'listOfTweets': listOfTweets,}
                
        template = JINJA_ENVIRONMENT.get_template('gamehype.html')
        self.response.write(template.render(template_values))        

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/gamehype', SingleGame),
], debug=True)
