import os
import json
import sys


if len(sys.argv) != 3:
	print sys.argv[0] + " <input_file_name> <output_file_name>"
	sys.exit(2)
input_file_name = sys.argv[1]
output_file_name = sys.argv[2]

output_file = open(output_file_name, "a")


def read_data(filename):
	data = []
	try:
		with open(filename, 'r') as f:
			for line in f:
				line = line.strip()
				if line:
					data.append (json.loads (line))
	except ValueError as detail:
		print "Error reading file: "+filename
		print str(detail)
		return []
	return data


def get_tweets():
    return read_data(os.path.join(os.getcwd(), input_file_name))


def transform_tweets(tweets):
	for tweet in tweets:
		if not 'limit' in tweet: # prevent parsing twitters 'limit' messages
			short_tweet = {
				"coordinates": tweet['coordinates'],
				"created_at": tweet["created_at"],
				"entities": { 
					'hashtags': tweet["entities"]["hashtags"]
					},
				"text": tweet["text"],
				 "user": {
				 	"screen_name": tweet['user']['screen_name'],
				 	"profile_image_url": tweet['user']['profile_image_url'],
				 	'followers_count': tweet['user']['followers_count']
				 	}}
			output_file.write (json.dumps (short_tweet) + '\n')

tweets = get_tweets()
transform_tweets(tweets)
