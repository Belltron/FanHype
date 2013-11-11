import os
import json
import sys


if len(sys.argv) != 3:
	print "tweet_transform.py <input_file_name> <output_file_name>"
	sys.exit(2)
input_file_name = sys.argv[1]
output_file_name = sys.argv[2]

output_file = open(output_file_name, "a")


def read_data(filename):
	data = []
	try:
		with open(filename) as f:
			for line in f:
				data.append (json.loads (line.strip()))
	except:
		print "Error reading file: "+filename
		return []
	return data


def get_tweets():
    return read_data(os.path.join(os.getcwd(), input_file_name))


def transform_tweets(tweets):
	for tweet in tweets:
		short_tweet = {
			"coordinates": tweet['coordinates'],
			"created_at": tweet["created_at"],
			"entities": { 
				'hashtags': tweet["entities"]["hashtags"]
				},
			"favorite_count": tweet["favorite_count"],
			"filter_level": tweet["filter_level"],
			"id": tweet["id"],
			"lang": tweet["lang"],
			"retweet_count": tweet["retweet_count"],
			"text": tweet["text"],
			 "user": {
			 	"screen_name": tweet['user']['screen_name'],
			 	"profile_img_url": tweet['user']['profile_image_url'],
			 	"verified": tweet['user']['verified'],
			 	'followers_count': tweet['user']['followers_count'],
			 	'friends_count': tweet['user']['friends_count']
			 	}}
		output_file.write (json.dumps (short_tweet) + '\n')


tweets = get_tweets()
transform_tweets(tweets)