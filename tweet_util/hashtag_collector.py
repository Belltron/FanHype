import tweepy
import json


class TweetCollector():
    def __init__(self):
        self.consumer_key = '77uv5wYRi4lOyBOfkdrmw'
        self.consumer_secret = '59SHeBIhXfRZWlwgaD6vmdIzzZ6hTxGkF8sdtsIBiQ'
        self.access_token_key = '1593582174-T44Tzc25PSMY5XdPi9Av0M2lZosRUxX325r3g32'
        self.access_token_secret = 'mQso4hh5yCmwn2Zfo7iBzbUMBP9uvi8imDDgmY0'

    def CollectTweets(self, query):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token_key, self.access_token_secret)
        api = tweepy.API(auth)
        
        tw = {}
        
        tweetList = []
        hashTagText = ""
        hashTags = []
        tagInfo = []
        location = ""
        tagTuples = []
        for tweet in tweepy.Cursor(api.search,
            q=query,
            rpp=100,
            result_type="recent",
            include_entities=True,
            lang="en").items(500):
            tw['entities'] = tweet.entities            
            tw['user'] = tweet.user
            tagInfo = ((tw['entities'])['hashtags'])
            for tag in tagInfo:
                hashTags.append(tag['text'])
        #print hashTags

        for tag in hashTags:
            count = hashTags.count(tag)
            tuple = (count,tag)
            if tuple not in tagTuples:
                tagTuples.append(tuple)

        tagTuples = sorted(tagTuples, key = lambda tup: -tup[0])
        for tup in tagTuples:
            print tup[1], '\t', tup[0]
        
            
        """
        #Print to file for testing purposes
        fileName = query + ".json"
        with open(fileName, 'w') as outfile:
            json.dump(tagTuples, outfile, indent = 0)
        """
        
if __name__ == "__main__":
    query = raw_input('Enter a Twitter query: ')
    collector = TweetCollector()
    collector.CollectTweets(query,)
