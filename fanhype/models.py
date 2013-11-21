from google.appengine.ext import ndb

class ApplicationData(ndb.Model):
    tweetText = ndb.StringProperty()
    #tweetTextList = ndb.StringProperty(repeated = True)
    date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def queryTweets(cls):
        return cls.query().order(-cls.date)

class Tweet(ndb.Model):
        coordinates = ndb.GeoPtProperty()
	tweetText = ndb.StringProperty()	
	hashTags = ndb.StringProperty()

        createdAt = ndb.StringProperty()
        favoriteCount = ndb.StringProperty()
        filterLevel = ndb.StringProperty()
        tweetId = ndb.StringProperty()
        lang = ndb.StringProperty()
        retweetCount = ndb.StringProperty()
        screenName = ndb.StringProperty()
        profileImgURL = ndb.StringProperty()
        verified = ndb.StringProperty()
        followersCount = ndb.StringProperty()
        friendsCount = ndb.StringProperty()
        latitude = ndb.StringProperty()
        longitude = ndb.StringProperty()
        game = ndb.StringProperty()
	
	date = ndb.DateTimeProperty(auto_now_add=True)

class HypeTable(ndb.Model):
    teamOneName = ndb.StringProperty()
    teamOneHype = ndb.StringProperty()
    teamOneTweetTotal = ndb.StringProperty()
    teamOneHashTags = ndb.StringProperty()
    teamTwoName = ndb.StringProperty()
    teamTwoHype = ndb.StringProperty()
    teamTwoTweetTotal = ndb.StringProperty()
    teamTwoHashTags = ndb.StringProperty()

class GeoData(ndb.Model):
    teamName = ndb.StringProperty()
    coordinates = ndb.StringProperty()

class TopTweet(ndb.Model):
    teamName = ndb.StringProperty()
    imageUrl = ndb.StringProperty()
    tweetText = ndb.StringProperty()
    userName = ndb.StringProperty()
    hypeScore = ndb.StringProperty()
    followerCount = ndb.StringProperty()

class LatestTweets(ndb.Model):
    teamName = ndb.StringProperty()
    imageUrl = ndb.StringProperty()
    tweetText = ndb.StringProperty()
    userName = ndb.StringProperty()
    hypeScore = ndb.StringProperty()
    createdAt = ndb.StringProperty()
    followerCount = ndb.StringProperty()
        
