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

def remove_tweets(tweets, team_one_tags, team_two_tags):
	team_one_tags = [tag.lower() for tag in team_one_tags]
	team_two_tags = [tag.lower() for tag in team_two_tags]
	
	for tweet in tweets:
		is_team_one = False
		is_team_two = False
		for hashtag in tweet['entities']['hashtags']:
			if hashtag['text'].lower() in team_one_tags:
				is_team_one = True
			if hashtag['text'].lower() in team_two_tags:
				is_team_two = True
		if (is_team_one and not is_team_two) or (is_team_two and not is_team_one):
			output_file.write (json.dumps (tweet) + '\n')

mizzou_tags = ['mizzou', 'beatauburn','gomizzou']
auburn_tags = ['wareagle','beatmizzou','aufamily','wardamneagle']
nebraska_tags = ['huskers','gobigred','cornhusker']
michigan_tags = ['goblue','bighouse','beatnebraska','wolverines']
baylor_tags = ['sicour','everyoneinblack','watchbu','sicem']
okie_tags = ['beatbaylor','boomersooner']

tweets = get_tweets()
remove_tweets(tweets, baylor_tags, okie_tags)



