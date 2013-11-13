import tweepy
import json
import config
from tweepy import OAuthHandler
from models import ApplicationData


class TweetCollector():
    def CollectTweets(self, query):
        c = config.Config()
        keys = c.get_keys()
        auth = OAuthHandler(keys[0], keys[1])
        auth.set_access_token(keys[2], keys[3])
        
        api = tweepy.API(auth)
        
        tw = {}
        
        tweetList = []
        tweetText = ""
        hashTags = []
        tagInfo = []
        tagTuples = []
        printList = []
        for tweet in tweepy.Cursor(api.search,
            q=query,
            rpp=100,
            result_type="recent",
            include_entities=True,
            lang="en").items(5):
            tweetText = tweet.text      #.encode('utf-8')           
            imageURL = tweet.user.profile_image_url_https       #.encode('utf-8')
            #printList.append((imageURL,tweetText))
            printList.append(tweetText)

        appData = ApplicationData()
        appData.tweetText = tweetText
        appData.put()
        
        print printList
        return printList
    
        
if __name__ == "__main__":
    texasAandMQuery = "Texas A&M"
    mississippiStateQuery = "Mississippi State"
    stanfordQuery = "Stanford"
    oregonQuery = "Oregon"
    baylorQuery = "Baylor"
    oklahomaQuery = "Oklahoma"
    
    texasAandMTags = ['gigem', 'aggies', '12thman']
    mississippiStateTags = ['mississippistate', 'hailstate', 'msstate']
    stanfordTags = ['stanford', 'beatuo', 'gostanford']
    oregonTags = ['goducks', 'oregonfootball', 'ducksfootball']
    baylorTags = ['everyoneinblack', 'sicou', 'baylor', 'sicem', 'sicembears']
    oklahomaTags = ['sooners', 'boomersooner', 'gosooners']
    
    collector = TweetCollector()
    #collector.CollectTweets(texasAandMQuery, texasAandMTags)
    #collector.CollectTweets(mississippiStateQuery, mississippiStateTags)
    #collector.CollectTweets(stanfordQuery, stanfordTags)
    #collector.CollectTweets(oregonQuery, oregonTags)
    #collector.CollectTweets(baylorQuery, baylorTags)
    collector.CollectTweets(oklahomaQuery)
