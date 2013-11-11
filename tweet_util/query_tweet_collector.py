import tweepy
import json


class TweetCollector():
    def __init__(self):
    	self.consumer_key = ''
	self.consumer_secret = ''
	self.access_token_key = ''
	self.access_token_secret = ''

    def CollectTweets(self, query, listofTags):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token_key, self.access_token_secret)
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
            lang="en").items(2000):
            tweetText = tweet.text.encode('utf-8')
            tw['entities'] = tweet.entities            
            tagInfo = ((tw['entities'])['hashtags'])
            for tag in tagInfo:
                tagText = tag['text']
                tagText = tagText.lower()
                if tagText in listofTags:
                    printList.append(tweetText)
        
        #Print to file for testing purposes
        fileName = query + ".json"
        with open(fileName, 'w') as outfile:
            json.dump(printList, outfile, indent = 0)
    
        
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
    collector.CollectTweets(oklahomaQuery, oklahomaTags)
