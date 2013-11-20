import json
import math
import os
import datetime
import time

def read_data(filename):
    """
    purpose: read all tweets from the json file.
    parameter: 
        filename - the path of json file in your local computer 
    return: a list containing all raw tweets each of which has the data structure of dictionary
    """
    data = []
    try:
        with open(filename) as f:
            for line in f:
                #print line
                if line not in ['\n', '\r\n']:
                    data.append(json.loads(line.strip()))
    except:
        print "Failed to read data!"
        return []
    print "The json file has been successfully read!"
    print str(len(data)) + " lines read."
    return data

class GameHype(object):
    def __init__(self, tweets, teamOneTags, teamTwoTags):
        self.tweets = tweets
        self.teamOneTags = [tag.lower() for tag in teamOneTags]
        self.teamTwoTags = [tag.lower() for tag in teamTwoTags]
        self.teamOneTotal = 0
        self.teamTwoTotal = 0
        self.teamOneBeforeKickoff = 0
        self.teamTwoBeforeKickoff = 0
        self.teamOneAfterKickoff = 0
        self.teamTwoAfterKickoff = 0
        self.total = 0
        self.gameTime = gameTime

    def getHype(self):
        with open('baylorOklahoma.json', 'w') as outfile:
            for tweet in tweets:
                tempCountOne = 0
                tempCountTwo = 0
                created_at = time.strptime((tweet['created_at']), "%a %b %d %H:%M:%S +0000 %Y")
                hashTags = (tweet['entities'])['hashtags']
                for hashTag in hashTags:
                    hashTagText = hashTag['text'].lower()
                    if hashTagText in self.teamOneTags and hashTagText not in self.teamTwoTags:
                        tempCountOne = 1
                    if hashTagText in self.teamTwoTags and hashTagText not in self.teamOneTags:
                        tempCountTwo = 1

                if tempCountOne == 1 and tempCountTwo == 0:
                    self.teamOneTotal += 1
                    outfile.write(json.dumps(tweet) + '\n')
                if tempCountOne == 0 and tempCountTwo == 1:
                    self.teamTwoTotal += 1
                    outfile.write(json.dumps(tweet) + '\n')
                    
        self.total = self.teamOneTotal + self.teamTwoTotal
        teamOneHype = float(self.teamOneTotal) / self.total * 100
        teamTwoHype = float(self.teamTwoTotal) / self.total * 100
        
        return (self.teamOneTotal, teamOneHype, self.teamTwoTotal, teamTwoHype)
        



if __name__=="__main__":
    gameTimeString = "Thu Nov 07 23:30:00 +0000 2013"
    gameTime = time.strptime(gameTimeString, "%a %b %d %H:%M:%S +0000 %Y")
    tweets = read_data(os.path.join(os.getcwd(),'bo_tweets.json'))
    team_one_name = 'Baylor'
    team_two_name = 'Oklahoma'
    team_one_tags = ['everyoneinblack', 'sicou', 'baylor', 'sicem', 'sicembears']
    team_two_tags = ['oklahoma','boomersooner', 'gosooners', 'beatbaylor']

    gameHype = GameHype(tweets, team_one_tags, team_two_tags)
    hypeTuple = gameHype.getHype()
    team_one_total = hypeTuple[0]
    team_one_hype = hypeTuple[1]    
    
    team_two_total = hypeTuple[2]
    team_two_hype = hypeTuple[3]

    
    
    print "Total Number of "+team_one_name+" hype tweets: ", team_one_total
    print "Total Number of "+team_two_name+" hype tweets: ", team_two_total
    print "All "+team_one_name+" Hype: ", int(team_one_hype), '\t', "All "+team_two_name+" Hype: ", int(team_two_hype)
    
