from models import Tweet
import logging

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

    def getHype(self):
        for tweet in self.tweets:
            tempCountOne = 0
            tempCountTwo = 0
            hashTags = []
            if tweet.hashTags != None and len(tweet.hashTags) > 1:
                hashTags = tweet.hashTags.split(',')
            for hashTag in hashTags:
                if hashTag in self.teamOneTags and hashTag not in self.teamTwoTags:
                    tempCountOne = 1
                if hashTag in self.teamTwoTags and hashTag not in self.teamOneTags:
                    tempCountTwo = 1

            if tempCountOne == 1 and tempCountTwo == 0:
                 self.teamOneTotal += 1
            if tempCountOne == 0 and tempCountTwo == 1:
                self.teamTwoTotal += 1
                    
        self.total = self.teamOneTotal + self.teamTwoTotal
        teamOneHype = float(self.teamOneTotal) / self.total * 100
        teamTwoHype = float(self.teamTwoTotal) / self.total * 100
        
        return (self.teamOneTotal, teamOneHype, self.teamTwoTotal, teamTwoHype)
