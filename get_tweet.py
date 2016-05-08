#! /usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import json
import requests
from requests_oauthlib import OAuth1
import signal
import threading
import yaml

from db_setup import db_connection
from db_setup import db_connect
from db_setup import db_insert_to_tweet

# STATIC GLOBAL OBJECT
api_key         = None 
api_secret      = None 
access_token    = None 
access_secret   = None 

def stream_setup():

    # USE db_connection
    global api_key
    global api_secret
    global access_token
    global access_secret

    try:
        # see:
        # http://blog.panicblanket.com/archives/1076
        f = open('setup.yml', 'r')
        data = yaml.load(f)
        f.close()

        api_key         = data['TWITTER']['api_key']
        api_secret      = data['TWITTER']['api_secret']
        access_token    = data['TWITTER']['access_token']
        access_secret   = data['TWITTER']['access_secret']

    except Exception as e:
        import sys
        print("[failure] Unexpected error:", e)
        quit()

    return

def stream_all():
    stream_setup()

    #
    #
    # TODO: Get words from db
    #
    #
    dict_list = ['スロット', '回胴', 'パチスロ', '#スロット', '#回胴', '#パチスロ', '#アニメ']
    track = ",".join(dict_list)

    url = "https://stream.twitter.com/1.1/statuses/filter.json"
    auth = OAuth1(api_key, api_secret, access_token, access_secret)
    r = requests.post(url, auth=auth, stream=True, data={"track":track})

    tweets = []

    #
    # TODO: Error Handling
    # see:
    # http://www.slideshare.net/yusukey/3twitter-api-api
    #

    for line in r.iter_lines():
        # filter out keep-alive new lines
        if line:
            #print(json.loads(line.decode()))
            #tweets.append(json.loads(line.decode()))

            #tweets.append(json.dumps(line.decode()))
            #print(json.dumps(line.decode()))

            print(json.dumps(json.loads(line.decode()), sort_keys=True,))
            tweets.append(json.dumps(json.loads(line.decode()), sort_keys=True,))
            print("Now tweets are ", len(tweets))

        #if len(tweets) >= 100:
        if len(tweets) >= 2:
            tweets_copy = copy.deepcopy(tweets)
            tweets = []
            thread = threading.Thread(target=db_insert_to_tweet, args=(tweets_copy,))  # Initialize
            thread.start() # Start

    return
# End of stream_all

def stream_sample():
    stream_setup()
    url = "https://stream.twitter.com/1.1/statuses/sample.json"
    auth = OAuth1(api_key, api_secret, access_token, access_secret)
    r = requests.get(url, auth=auth, stream=True)
    for line in r.iter_lines():
        # filter out keep-alive new lines
        if line:
            print(json.loads(line.decode()))
    return
# End of stream_sample

# 異常終了時の処理
def signal_handler(sig, stack):
    if db_connection is not None:
        db_connection.close()

    print('signal_handler(): %d, %s' % (sig, str(stack)))
    raise SystemExit('Exiting')
    return
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGUSR1, signal_handler)

if __name__ == '__main__':

    try:
        db_connect()
        #stream_sample()
        stream_all()
    except:
        print("Error is occured..")
        quit()
    finally:
        db_connection.close()

