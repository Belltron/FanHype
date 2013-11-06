import tweepy
import json


class TweetCollector():
    def __init__(self):
    	self.consumer_key = ''
	self.consumer_secret = ''
	self.access_token_key = ''
	self.access_token_secret = ''

    def CollectTweets(self, query, docID):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token_key, self.access_token_secret)
        api = tweepy.API(auth)
        
        tw = {}
        
        tweetList = []
        hashTagText = ""
        hashTags = []
        tagInfo = []
        location = ""
        for tweet in tweepy.Cursor(api.search,
            q=query,
            rpp=100,
            result_type="recent",
            include_entities=True,
            lang="en").items(20):
            tw['entities'] = tweet.entities            
            tw['user'] = tweet.user
            print tweet.coordinates
            #location = (tweet.user)['location']
            #print location
            tagInfo = ((tw['entities'])['hashtags'])
            for tag in tagInfo:
                hashTags.append(tag['text'])
        #print hashTags
        """
        #Print to file for testing purposes
        fileName = docID + ".json"
        with open(fileName, 'w') as outfile:
            json.dump(printList, outfile)
        """   
        
if __name__ == "__main__":
    query = raw_input('Enter a Twitter query: ')
    collector = TweetCollector()
    collector.CollectTweets(query, 'johnny football')
