#!/usr/bin/python

import sys
import csv
from twitter import *
import redis
from pprint import pprint

# handles csv

if len(sys.argv) < 3 or sys.argv[1] == '-h':
    print "Usage: "+sys.argv[0]+" [twitter_cfg.py] @user"
    sys.exit(0)

tw_cfg = sys.argv[1].replace('.py', '')
user_id = sys.argv[2]
handles = []

try:
    cfg = __import__(tw_cfg)
except:
    print "Couldn't import config: %s" % owner_cfg

auth = OAuth(cfg.access_key, cfg.access_secret, cfg.consumer_key, cfg.consumer_secret)
twitter = Twitter(auth = auth)

try:
    results = twitter.statuses.mentions(screen_name=user_id)
    for r in results:
        pprint(r)
    sys.exit()
except Exception, e:
    print "Error accessing: %r" % (e) 


