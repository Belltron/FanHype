from google.appengine.ext import ndb
class ApplicationData(ndb.Model):
    tweetText = ndb.StringProperty()
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
    teamOneHashTags = ndb.StringProperty()
    teamTwoHashTags = ndb.StringProperty()
    teamOneHype = ndb.FloatProperty()
    teamTwoHype = ndb.FloatProperty()
    teamOneName = ndb.StringProperty()
    teamTwoName = ndb.StringProperty()
    teamOneTweetTotal = ndb.IntegerProperty()
    teamTwoTweetTotal = ndb.IntegerProperty()
    teamOneColor = ndb.StringProperty()
    teamTwoColor = ndb.StringProperty()
    teamOneImage = ndb.StringProperty()
    teamTwoImage = ndb.StringProperty()
    gameTitle = ndb.StringProperty()
    gameTime = ndb.StringProperty()
    gameLocation = ndb.StringProperty()

class GeoData(ndb.Model):
    coordinates = ndb.StringProperty(indexed=False)
    teamName = ndb.StringProperty()

class TopTweet(ndb.Model):
    teamName = ndb.StringProperty()
    imageUrl = ndb.StringProperty()
    tweetText = ndb.StringProperty()
    userName = ndb.StringProperty()
    hypeScore = ndb.StringProperty()
    followerCount = ndb.StringProperty()

class LatestTweets(ndb.Model):
    teamName  = ndb.StringProperty()
    imageUrl = ndb.StringProperty()
    tweetText = ndb.StringProperty()
    userName = ndb.StringProperty()
    hypeScore = ndb.StringProperty()
    createdAt = ndb.StringProperty()
    followerCount = ndb.StringProperty()

def initializeModels():
	newHype = HypeTable()
	newHype.teamOneHashTags = 'everyoneinblack,sicou,baylor,sicem,sicembears'
	newHype.teamOneHype = 0
	newHype.teamOneName = 'Baylor'
	newHype.teamOneTweetTotal = 0
	newHype.teamTwoHashTags = 'oklahoma,boomersooner,gosooners,beatbaylor,ou'
	newHype.teamTwoHype = 0
	newHype.teamTwoName = 'Oklahoma'
	newHype.teamTwoTweetTotal = 0
	newHype.put()

	newGeoData = GeoData()
	newGeoData.coordinates = ''
	newGeoData.teamName = 'Baylor'
	newGeoData.put()

	newGeoData = GeoData()
	newGeoData.coordinates = ''
	newGeoData.teamName = 'Oklahoma'
	newGeoData.put()

"""
    Point class is used to render latitude/longitude values to the
        html for the heatmap to use. This model isn't stored in the
        datastore.
"""
class Point(object):
    def __init__(self, lat_lon_string):
        if len(lat_lon_string) > 0:
            lat_lon   = lat_lon_string.split(',')
            self.longitude  = lat_lon[0]
            self.latitude = lat_lon[1]
        else:
            self.longitude = 0
            self.latitude = 0



