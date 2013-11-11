import json
from collections import defaultdict
import re
from stemming import porter2
import math
import random
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
    return data

class GameHype(object):
    def __init__(self, tweets, teamOneTags, teamTwoTags, gameTime):
        self.tweets = tweets
        self.teamOneTags = teamOneTags
        self.teamTwoTags = teamTwoTags
        self.teamOneTotal = 0
        self.teamTwoTotal = 0
        self.teamOneBeforeKickoff = 0
        self.teamTwoBeforeKickoff = 0
        self.teamOneAfterKickoff = 0
        self.teamTwoAfterKickoff = 0
        self.total = 0
        self.gameTime = gameTime

    def getHype(self):
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
            if tempCountOne == 1 and tempCountTwo == 0 and created_at < self.gameTime:
                self.teamOneBeforeKickoff += 1
            if tempCountOne == 0 and tempCountTwo == 1 and created_at < self.gameTime:
                self.teamTwoBeforeKickoff += 1
            if tempCountOne == 1 and tempCountTwo == 0 and created_at >= self.gameTime:
                self.teamOneAfterKickoff += 1
            if tempCountOne == 0 and tempCountTwo == 1 and created_at >= self.gameTime:
                self.teamTwoAfterKickoff += 1

        self.teamOneTotal = self.teamOneBeforeKickoff + self.teamOneAfterKickoff
        self.teamTwoTotal = self.teamTwoBeforeKickoff + self.teamTwoAfterKickoff
        totalBefore = self.teamOneBeforeKickoff + self.teamTwoBeforeKickoff
        totalAfter = self.teamOneAfterKickoff + self.teamTwoAfterKickoff

        self.total = self.teamOneTotal + self.teamTwoTotal
        teamOneHype = float(self.teamOneTotal) / self.total * 100
        teamTwoHype = float(self.teamTwoTotal) / self.total * 100
        
        teamOneHypeBefore = float(self.teamOneBeforeKickoff) / totalBefore * 100
        teamTwoHypeBefore = float(self.teamTwoBeforeKickoff) / totalBefore * 100

        teamOneHypeAfter = float(self.teamOneAfterKickoff) / totalAfter * 100
        teamTwoHypeAfter = float(self.teamTwoAfterKickoff) / totalAfter * 100
        return (self.teamOneTotal, teamOneHype, teamOneHypeBefore, teamOneHypeAfter,
                self.teamTwoTotal, teamTwoHype, teamTwoHypeBefore, teamTwoHypeAfter)
        



if __name__=="__main__":
    gameTimeString = "Sat Nov 09 19:30:00 +0000 2013"
    gameTime = time.strptime(gameTimeString, "%a %b %d %H:%M:%S +0000 %Y")
    tweets = read_data(os.path.join(os.getcwd(),'tweets.json'))
    nebraskaTags = ['huskers', 'gobigred', 'cornhuskers', 'beatmichigan']
    michiganTags = ['goblue','bighouse','beatnebraska','wolverines']
    gameHype = GameHype(tweets, nebraskaTags, michiganTags, gameTime)
    hypeTuple = gameHype.getHype()
    nebraskaTotal = hypeTuple[0]
    nebraskaHype = hypeTuple[1]
    nebraskaHypeBefore = hypeTuple[2]
    nebraskaHypeAfter = hypeTuple[3]
    
    
    michiganTotal = hypeTuple[4]
    michiganHype = hypeTuple[5]
    michiganHypeBefore = hypeTuple[6]
    michiganHypeAfter = hypeTuple[7]
    
    
   
    

    print "Total Number of Nebraska 'hype' tweets: ", nebraskaTotal
    print "Total Number of Michigan 'hype' tweets: ", michiganTotal
    print "Nebraska Hype before kickoff: ", int(nebraskaHypeBefore), '\t', "Michigan Hype before kickoff: ", int(michiganHypeBefore)
    print "Nebraska Hype after kickoff: ", int(nebraskaHypeAfter), '\t', "Michigan Hype after kickoff: ", int(michiganHypeAfter)
    print "All Nebraska Hype: ", int(nebraskaHype), '\t', "All Michigan Hype: ", int(michiganHype)
    
