import json
import sys
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from twython import Twython
import config

class StdOutListener(StreamListener):

	def __init__(self):
		self.stanford_sum = 0
		self.oregon_sum = 0
		self.stanford_tags = ['#stanford', '#gostanford', '#beatou', '#beatoregon']
		self.oregon_tags = ['#ou', '#oregonfootball', '#ducksfootball', '#goducks', '#beatstanford']

	def on_data(self, data):
		tweet = json.loads(data)
		
		found = False
		for tag in self.stanford_tags:
			if tag in tweet['text'].lower():
				found = True

		if found:
			self.stanford_sum += 1
		else:
			self.oregon_sum += 1

		print tweet['created_at']
		print tweet['text']

		stanford_p = float(100*self.stanford_sum)/(self.stanford_sum+self.oregon_sum)
		oregon_p = float(100*self.oregon_sum)/(self.stanford_sum+self.oregon_sum)

		print 'stanford: ' + str(stanford_p) + '%' 
		print 'oregon: ' + str(oregon_p) + '%'

		print '         -------------'
		sys.stdout.write('stanford |')
		for i in range(int(stanford_p/10)):
			sys.stdout.write(' ')
		sys.stdout.write('|')
		for i in range(10 - int(stanford_p/10)):
			sys.stdout.write(' ')
		print '| oregon'
		print '         -------------'
		return True

	def on_error(self, status):
		print status

c = config.Config()
keys = c.get_keys()

auth = OAuthHandler(keys[0], keys[1])
auth.set_access_token(keys[2], keys[3])

l = StdOutListener()

stream = Stream(auth, l)
# hashtags by game
stanford_oregon = ['#gostanford', '#beatou', '#beatoregon', '#stanford',  '#ou', '#oregonfootball', '#ducksfootball', '#goducks', '#beatstanford']
baylor_oklahoma = []
tamu_msstate = []

stream.filter(track=stanford_oregon)