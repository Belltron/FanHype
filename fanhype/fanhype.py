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
	coordinates = ndb.GeoPtProperty()
	date = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):
        def get(self):                
                template = JINJA_ENVIRONMENT.get_template('index.html')
                self.response.write(template.render(title = "lol"))
                #self.response.write(MAIN_PAGE_HTML)

                self.response.write('<html><body>')
		self.response.write('<h1>Hello, World!</h1>')
                tweet_query = Tweet.query()
                tweets = tweet_query.fetch()
                for tweet in tweets:
			self.response.write('<p>Page hit at: <b>%s</b></p>' % tweet.date)
		self.response.write('</body></html>')
		
                new_tweet = Tweet()
		new_tweet.screen_name = 'Sample Text'
		new_tweet.coordinates = ndb.GeoPt(-36.654, 26.546)
		new_tweet.put()

		
class SingleGame(webapp2.RequestHandler):
    def post(self):        
        template = JINJA_ENVIRONMENT.get_template('gamehype.html')
        self.response.write(template.render(title = "lol"))
        collector = TweetCollector()
        query = "Nebraska"
        listOfTweetTuples = collector.CollectTweets(query)
        self.response.write('<html><body>')
        for tweet in listOfTweetTuples:
                self.response.write('<p>')
                self.response.write('<p style="float: left;"><img src=%s height="32px" width="32px" border="1px"></p>' % tweet[0])
                self.response.write('<p>%s<br><br><br></p>' % tweet[1])
                self.response.write('</p>')
        self.response.write('</body></html>')
        #self.response.write('<html><body>Nebraska vs. Michigan:<pre>')
        #self.response.write(cgi.escape(self.request.get('content')))
        #self.response.write('</pre></body></html>')

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/gamehype', SingleGame),
], debug=True)
