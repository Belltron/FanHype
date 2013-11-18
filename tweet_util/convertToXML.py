import json
import math
import os
import datetime
import time
import xml.dom.minidom

def read_data(filename):
    """
    purpose: read all tweets from the json file.
    parameter: 
        filename - the path of json file in your local computer 
    return: a list containing all raw tweets each of which has the data structure of dictionary
    """
    data = []
    try:
        with open(filename) as f:
            for line in f:
                #print line
                if line not in ['\n', '\r\n']:
                    data.append(json.loads(line.strip()))
    except:
        print "Failed to read data!"
        return []
    print "The json file has been successfully read!"
    print str(len(data)) + " lines read."
    
    return data

if __name__=="__main__":
    tweets = read_data(os.path.join(os.getcwd(),'tweets.json'))
    print "Tweet length: ", len(tweets)
    doc = "<tweets>"
    for tweet in (tweets):
        #print index + 1
        tweetText = tweet['text']
        geo = tweet['geo']
        if geo is not None:
            coordinates = (tweet['geo'])['coordinates']        
        hashTags = (tweet['entities'])['hashtags']
        
        createdAt = tweet['created_at']
        favoriteCount = tweet['favorite_count']
        filterLevel = tweet['filter_level']
        tweetId = tweet['id']
        lang = tweet['lang']
        retweetCount = tweet['retweet_count']
        screenName = tweet['user']['screen_name']
        profileImgURL = tweet['user']['profile_image_url']
        verified = tweet['user']['verified']
        followersCount = tweet['user']['followers_count']
        friendsCount = tweet['user']['friends_count']


        
        doc += "<tweet>"
        doc += "<coordinates>"
        if geo is not None:
            doc += "["
            doc += str(coordinates[0])
            doc += ","
            doc += str(coordinates[1])
            doc += "]"
        doc += "</coordinates>"
        doc += "<tweetText>"
        doc += tweetText
        doc += "</tweetText>"
        doc += "<hashTags>"        
        if len(hashTags) != 0:
            doc += "["
            for iter, hashTag in enumerate(hashTags):
                doc += hashTag['text'].lower()
                if iter == len(hashTags) - 1:
                    doc += "]"
                else:
                    doc += ","
        doc += "</hashTags>"        

        doc += "<createdAt>"
        doc += createdAt
        doc += "</createdAt>"
        doc += "<favoriteCount>"
        doc += str(favoriteCount)
        doc += "</favoriteCount>"
        doc += "<filterLevel>"
        doc += filterLevel
        doc += "</filterLevel>"
        doc += "<tweetId>"
        doc += str(tweetId)
        doc += "</tweetId>"
        doc += "<lang>"
        doc += lang
        doc += "</lang>"
        doc += "<retweetCount>"
        doc += str(retweetCount)
        doc += "</retweetCount>"
        doc += "<screenName>"
        doc += screenName
        doc += "</screenName>"
        doc += "<profileImgURL>"
        doc += profileImgURL
        doc += "</profileImgURL>"
        doc += "<verified>"
        doc += str(verified)
        doc += "</verified>"
        doc += "<followersCount>"
        doc += str(followersCount)
        doc += "</followersCount>"
        doc += "<friendsCount>"
        doc += str(friendsCount)
        doc += "</friendsCount>"

        doc += "</tweet>"

        
    doc += "</tweets>"
    xml = (xml.dom.minidom.parseString(doc))
    out = str(xml.toprettyxml(indent = '   '))
    fileName = "xmlGen.xml"
    with open(fileName, 'w') as outfile:
        outfile.write(out)
