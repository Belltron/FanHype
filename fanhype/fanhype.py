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

class Data(webapp2.RequestHandler):
	def get(self):
		self.response.write('<html><head><script src="js/app.js" type="text/javascript" ></script></head><body><p>hello</p></body></html>')
		#data = '{"created_at":"Sat Nov 09 00:33:41 +0000 2013","id":398971622310559744,"id_str":"398971622310559744","text":"RT if you love Austin  #voteaustinmahone","source":"\u003ca href=\"http:\/\/twitter.com\/download\/iphone\" rel=\"nofollow\"\u003eTwitter for iPhone\u003c\/a\u003e","truncated":false,"in_reply_to_status_id":null,"in_reply_to_status_id_str":null,"in_reply_to_user_id":null,"in_reply_to_user_id_str":null,"in_reply_to_screen_name":null,"user":{"id":175148033,"id_str":"175148033","name":"alexis","screen_name":"AlexisMahone22","location":"","url":null,"description":"One boy by the name of Austin Carter Mahone changed my life\u2764\ufe0f Austin followed me 1\/17\/13. Alex RT.D me 7\/11\/12. I met Austin 9\/27\/13 & he called me beautiful!","protected":false,"followers_count":1496,"friends_count":1821,"listed_count":3,"created_at":"Thu Aug 05 19:23:13 +0000 2010","favourites_count":614,"utc_offset":-21600,"time_zone":"Central Time (US & Canada)","geo_enabled":true,"verified":false,"statuses_count":4087,"lang":"en","contributors_enabled":false,"is_translator":false,"profile_background_color":"FF1A00","profile_background_image_url":"http:\/\/abs.twimg.com\/images\/themes\/theme10\/bg.gif","profile_background_image_url_https":"https:\/\/abs.twimg.com\/images\/themes\/theme10\/bg.gif","profile_background_tile":false,"profile_image_url":"http:\/\/pbs.twimg.com\/profile_images\/378800000700707698\/64ccda41acbc7a3406495e244cef1791_normal.jpeg","profile_image_url_https":"https:\/\/pbs.twimg.com\/profile_images\/378800000700707698\/64ccda41acbc7a3406495e244cef1791_normal.jpeg","profile_banner_url":"https:\/\/pbs.twimg.com\/profile_banners\/175148033\/1383359945","profile_link_color":"FF0000","profile_sidebar_border_color":"FFFFFF","profile_sidebar_fill_color":"7AC3EE","profile_text_color":"3D1957","profile_use_background_image":true,"default_profile":false,"default_profile_image":false,"following":null,"follow_request_sent":null,"notifications":null},"geo":{"type":"Point","coordinates":[40.64283364,-77.55032645]},"coordinates":{"type":"Point","coordinates":[-77.55032645,40.64283364]},"place":{"id":"881cf2186bfb1d9f","url":"https:\/\/api.twitter.com\/1.1\/geo\/id\/881cf2186bfb1d9f.json","place_type":"city","name":"Burnham","full_name":"Burnham, PA","country_code":"US","country":"United States","contained_within":[],"bounding_box":{"type":"Polygon","coordinates":[[[-77.577475,40.621549],[-77.577475,40.647654],[-77.546701,40.647654],[-77.546701,40.621549]]]},"attributes":{}},"contributors":null,"retweet_count":0,"favorite_count":0,"entities":{"hashtags":[{"text":"voteaustinmahone","indices":[23,40]}],"symbols":[],"urls":[],"user_mentions":[]},"favorited":false,"retweeted":false,"filter_level":"medium","lang":"en"}'
		#self.response.write(data)


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/data', Data),
], debug=True)
