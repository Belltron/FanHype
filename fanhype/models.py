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
	hashTags = ndb.StringProperty(repeated=True)

        createdAt = ndb.DateTimeProperty()
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
	
	date = ndb.DateTimeProperty(auto_now_add=True)
        
