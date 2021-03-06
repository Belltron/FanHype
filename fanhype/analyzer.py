from models import Tweet
import logging
import math

def calculateHype(tweets, teamOneTags, teamTwoTags):

    teamOneTags = [tag.lower() for tag in teamOneTags]
    teamTwoTags = [tag.lower() for tag in teamTwoTags]
    teamOneTotal = 0
    teamTwoTotal = 0
    total = 0

    for tweet in tweets:
        tempCountOne = 0
        tempCountTwo = 0
        hashTags = []
        if tweet.hashTags != None and len(tweet.hashTags) > 1:
            hashTags = tweet.hashTags.split(',')
        for hashTag in hashTags:
            if hashTag in teamOneTags and hashTag not in teamTwoTags:
                tempCountOne = 1
            if hashTag in teamTwoTags and hashTag not in teamOneTags:
                tempCountTwo = 1

        if tempCountOne == 1 and tempCountTwo == 0:
            teamOneTotal += 1
        if tempCountOne == 0 and tempCountTwo == 1:
            teamTwoTotal += 1
                
    total = teamOneTotal + teamTwoTotal

    if total != 0:
        teamOneHype = float(teamOneTotal) / total * 100
        teamTwoHype = float(teamTwoTotal) / total * 100
    else:
        teamOneHype = 0
        teamTwoHype = 0
    
    return (teamOneTotal, teamOneHype, teamTwoTotal, teamTwoHype)

def calculateHypeJson(tweet, teamOneTags, teamTwoTags):

    teamOneTags = [tag.lower() for tag in teamOneTags]
    teamTwoTags = [tag.lower() for tag in teamTwoTags]
    usedtags = []
    teamOneTotal = 0
    teamTwoTotal = 0
    total = 0

    tempCountOne = 0
    tempCountTwo = 0
    teamOneTagScore = 0
    teamTwoTagScore = 0
    for hashTag in tweet['entities']['hashtags']:
        if hashTag['text'].lower() in teamOneTags and hashTag['text'].lower() not in teamTwoTags:
            tempCountOne = 1
            if hashTag['text'].lower() not in usedtags:
                teamOneTagScore += 1
                usedtags.append(hashTag['text'].lower())
        if hashTag['text'].lower() in teamTwoTags and hashTag['text'].lower() not in teamOneTags:
            tempCountTwo = 1
            if hashTag['text'].lower() not in usedtags:
                teamTwoTagScore += 1
                usedtags.append(hashTag['text'].lower())

    if (tempCountOne and tempCountTwo) or tweet['user']['followers_count'] == 0:
        return (0,0)

    #tempCountOne *= math.log(1 + (tweet['user']['followers_count'])*teamOneTagScore/500.0, 2)
    #tempCountTwo *= math.log(1 + (tweet['user']['followers_count'])*teamTwoTagScore/500.0, 2)

    tempCountOne = math.log(1 + teamOneTagScore, 2) * math.log(1 + (tweet['user']['followers_count']), 5)
    tempCountTwo = math.log(1 + teamTwoTagScore, 2) * math.log(1 + (tweet['user']['followers_count']), 5)

        
    return (tempCountOne,tempCountTwo)