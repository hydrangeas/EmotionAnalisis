#! /usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
import requests
from requests_oauthlib import OAuth1

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

    url = "https://stream.twitter.com/1.1/statuses/filter.json"
    auth = OAuth1(api_key, api_secret, access_token, access_secret)
    #r = requests.post(url, auth=auth, stream=True, data={"follow":"nasa9084","track":"emacs"})
    r = requests.post(url, auth=auth, stream=True, data={"track":"天気"})
    
    for line in r.iter_lines():
        #print(line["text"])
        print(line)

    return
# End of stream_all

if __name__ == '__main__':
    stream_all();




