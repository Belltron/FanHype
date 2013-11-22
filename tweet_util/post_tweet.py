import urllib
import urllib2
import os
import sys
import json


if len(sys.argv) != 2:
    print sys.argv[0] + " <input_file_name>"
    sys.exit(2)
input_file_name = sys.argv[1]


def read_data(filename):
    data = []
    try:
        with open(filename) as f:
            for line in f:
                data.append (json.loads (line.strip()))
    except:
        print "Error reading file: "+filename
        return []
    return data


def get_tweets():
    return read_data(os.path.join(os.getcwd(), input_file_name))


def send_tweets():
    url = 'http://localhost:9080/savetweet'

    tweets = get_tweets()
    data = json.dumps(tweets)
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    response = urllib2.urlopen(req)
    the_page = response.read()


send_tweets()
