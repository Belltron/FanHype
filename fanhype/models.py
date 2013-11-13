from google.appengine.ext import ndb

class ApplicationData(ndb.Model):
    tweetText = ndb.StringProperty()
    #tweetTextList = ndb.StringProperty(repeated = True)
    date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def queryTweets(cls):
        return cls.query().order(-cls.date)
        
