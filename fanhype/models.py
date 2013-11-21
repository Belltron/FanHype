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
    teamOneHashTags = ndb.StringProperty()
    teamTwoHashTags = ndb.StringProperty()
    teamOneHype = ndb.FloatProperty()
    teamTwoHype = ndb.FloatProperty()
    teamOneName = ndb.StringProperty()
    teamTwoName = ndb.StringProperty()
    teamOneTweetTotal = ndb.IntegerProperty()
    teamTwoTweetTotal = ndb.IntegerProperty()
    """
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
    """

class GeoData(ndb.Model):
    coordinates = ndb.StringProperty()
    teamName = ndb.StringProperty()
    """
        newGeoData = GeoData()
        newGeoData.coordinates = '-33.343,45.234|41.342,56.454|'
        newGeoData.teamName = 'teamName'
        newGeoData.put()
    """









        
