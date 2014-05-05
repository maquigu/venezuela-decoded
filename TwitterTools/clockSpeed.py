#!/usr/bin/python

import csv
from datetime import datetime
import sys
from couchdb import Server
from twitter import *
from pprint import pprint
from TwitterSpeed import TwitterSpeed
import logging as log

log.basicConfig(filename=sys.argv[0]+'.log',level=log.DEBUG)

if len(sys.argv) < 3 or sys.argv[1] == '-h':
    print "Usage: "+sys.argv[0]+" [twitter_cfg.py] [userlist] [sample size]"
    sys.exit(0)

tw_cfg = sys.argv[1].replace('.py', '')
user_csv = sys.argv[2]
try:
    count = sys.argv[3]
except:
    count = 15

try:
    cfg = __import__(tw_cfg)
    users = csv.reader(open(user_csv, 'r'))
except:
    print "Couldn't import config: %s" % owner_cfg

couch = Server()
if 'speeds' not in couch:
    couch.create('speeds')
db = couch['speeds']
auth = OAuth(cfg.access_key, cfg.access_secret, cfg.consumer_key, cfg.consumer_secret)
twitter = Twitter(auth = auth)

s=TwitterSpeed(twitter, count)

for row in users:
    user = row[0]
    reach =  s.reach(user)
    activity = s.activity(user)
    a2r = s.a2r(user)
    r2a = s.r2a(user)
    now = datetime.now().isoformat()
    id = now+'_'+user
    uspeed = {
        'user': user,
        'timestamp': now,
        'reach': reach, 
        'activity': activity, 
        'a2r': a2r, 
        'r2a': r2a,
        'count': count
    }
    db[id] = uspeed
