#!/usr/bin/env python
# web server for tweet search
# You should not need to edit this file.

import time
import fileinput
import json
import bottle
import os
import sys

data_filename = sys.argv[1]
print data_filename

def read_data(filename):
    data = []
    try:
        with open(filename) as f:
            for line in f:
                data.append(json.loads(line.strip()))
    except:
        print "Error reading file. Usage:   python serve.py input_file.json"
        return []
    return data


def get_tweets():
    return read_data(os.path.join(os.getcwd(),data_filename))


@bottle.route('/search')
def search(name='World'):
    query = bottle.request.query.q
    start_time = time.time()
    tweets = get_tweets()
    end_time = time.time()

    return dict(
            tweets = tweets
        )

@bottle.route('/')
def index():
    return bottle.static_file('index.html', root='static')


@bottle.route('/favicon.ico')
def favicon():
    return bottle.static_file('favicon.ico', root='static')


@bottle.route('/static/<filename:path>')
def server_static(filename):
    return bottle.static_file(filename, root='static')

if __name__=="__main__":
	bottle.run(host='localhost',
               port=8080,
               reloader=True)