from google.appengine.ext import ndb

class ApplicationData(ndb.Model):
    tweetTextList = ndb.StringProperty(repeated=True)

    @staticmethod
    def setTweetTextList(tList):
        tweetTextList = tList

    def getTweetTextList():
        return tweetTextList
