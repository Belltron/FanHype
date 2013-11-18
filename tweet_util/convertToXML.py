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
    fileName = "xmlGen.xml"
    #doc = "<tweets>"
    with open(fileName, 'w') as outfile:
        outfile.write(json.dumps('<?xml version='+'"'+'1.0"'+'?>') + '\n') 
        #outfile.write("<?xml version="+'"'+'1.0"'+"?>\n") 
        #outfile.write("<tweets>\n")
        outfile.write(json.dumps('<Tweets>') + '\n')
        for tweet in (tweets):
            doc = ""
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


            
            doc += "<Tweet>"
            doc += "<coordinates>"
            if geo is not None:
                doc += str(coordinates[0])
                doc += ","
                doc += str(coordinates[1])
            doc += "</coordinates>"
            doc += "<tweetText>"
            doc += tweetText.encode('utf-8')
            doc += "</tweetText>"
            doc += "<hashTags>"        
            if len(hashTags) != 0:
                for iter, hashTag in enumerate(hashTags):
                    doc += hashTag['text'].lower().encode('utf-8')
                    if iter != len(hashTags) - 1:
                        doc += ","
            doc += "</hashTags>"        

            doc += "<createdAt>"
            doc += createdAt.encode('utf-8')
            doc += "</createdAt>"
            doc += "<favoriteCount>"
            doc += str(favoriteCount).encode('utf-8')
            doc += "</favoriteCount>"
            doc += "<filterLevel>"
            doc += filterLevel.encode('utf-8')
            doc += "</filterLevel>"
            doc += "<tweetId>"
            doc += str(tweetId).encode('utf-8')
            doc += "</tweetId>"
            doc += "<lang>"
            doc += lang.encode('utf-8')
            doc += "</lang>"
            doc += "<retweetCount>"
            doc += str(retweetCount).encode('utf-8')
            doc += "</retweetCount>"
            doc += "<screenName>"
            doc += screenName.encode('utf-8')
            doc += "</screenName>"
            doc += "<profileImgURL>"
            doc += profileImgURL.encode('utf-8')
            doc += "</profileImgURL>"
            doc += "<verified>"
            doc += str(verified).encode('utf-8')
            doc += "</verified>"
            doc += "<followersCount>"
            doc += str(followersCount).encode('utf-8')
            doc += "</followersCount>"
            doc += "<friendsCount>"
            doc += str(friendsCount).encode('utf-8')
            doc += "</friendsCount>"
            doc += "<date>2013-11-18T06:18:51</date>"

            doc += "</Tweet>"
            #outfile.write(doc)
            outfile.write(json.dumps(doc) + '\n')
        #outfile.write("</tweets>")
        outfile.write(json.dumps("</Tweets>"))
    """ 
    doc += "</Tweets>"
    
    xml = (xml.dom.minidom.parseString(doc))
    out = str(xml.toprettyxml(indent = '   '))
    
    with open(fileName, 'w') as outfile:
        outfile.write(out)
    """
