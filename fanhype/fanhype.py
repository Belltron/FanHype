import webapp2
from google.appengine.ext import ndb


class Tweet(ndb.Model):
	screen_name = ndb.StringProperty(indexed=False)
	coordinates = ndb.GeoPtProperty()
	date = ndb.DateTimeProperty(auto_now_add=True)

class MainPage(webapp2.RequestHandler):

	def get(self):
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


application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
