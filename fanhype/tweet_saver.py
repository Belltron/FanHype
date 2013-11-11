import json
import sys
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import config

class StdOutListener(StreamListener):

	def __init__(self):
		x = 1

	def on_data(self, data):
		sys.stdout.write(data)
		sys.stdout.flush()
		return True

	def on_error(self, status):
		print status

keys = config.Config().get_keys()
auth = OAuthHandler(keys[0], keys[1])
auth.set_access_token(keys[2], keys[3])

stream = Stream(auth, StdOutListener())

# hashtags by game
stanford_oregon = ['#gostanford', '#beatou', '#beatoregon', '#stanford',  '#ou', '#oregonfootball', '#ducksfootball', '#goducks', '#beatstanford']
baylor_oklahoma = ['#Baylor', '#SicEm', '#SicEmBears', '#WatchBU', '#EveryoneInBlack', '#SicOU', '#Sooners', '#BeatBaylor', '#BoomerSooner', '#gosooners']	
tamu_msstate = ['#gigem', '#aggies', '12thMan', '#mississippistate', '#hailstate', '#msstate']

stream.filter(track=stanford_oregon)