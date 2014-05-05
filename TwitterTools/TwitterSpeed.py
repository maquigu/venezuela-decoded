#!/usr/bin/python

import dateutil.parser
import time
from twitter import *
import logging as log

class TwitterSpeed:

    user = None
    count = None
    twitter_instance = None

    def __init__(self, twitter_instance, count=15):
        self.count = count
        self.twitter_instance = twitter_instance

    def reach(self, user, count=count):
        reach = None
        start_date = None
        end_date = None
        start_date_noted = False
        status_ctr = 0
        try:
            log.debug("Calculating mentions speed:")
            results = self.twitter_instance.search.tweets(q="%s"%user, count=count)
            for r in results['statuses']:
                if start_date_noted is False:
                    start_date=r['created_at']
                    start_date_noted=True
                end_date = r['created_at']
                status_ctr += 1
            log.debug("Start Date: " + start_date)
            log.debug("End Date: " + end_date)
            log.debug("Ctr:" + str(status_ctr))
            sd = int(time.mktime(dateutil.parser.parse(start_date).timetuple()))
            ed = int(time.mktime(dateutil.parser.parse(end_date).timetuple()))
            delta = sd-ed
            if delta == 0:
                delta = 1
            log.debug("Delta secs.: " + str(delta))
            if status_ctr <= 1:
                status_ctr = .0000000001
            reach = 60*(float(status_ctr)/delta)
            log.debug("Mentions: " + str(reach) + " tweets/minute")
        except Exception, e:
            log.debug("Error accessing: %r" % (e))
        return reach

    def activity(self, user, count=count):
        activity = None
        start_date = None
        end_date = None
        start_date_noted = False
        status_ctr = 0
        try:
            status_ctr = 0
            log.debug("Calculating activity speed:")
            results = self.twitter_instance.statuses.user_timeline(screen_name="%s"%user, count=count)
            for r in results:
                if start_date_noted is False:
                    start_date=r['created_at']
                    start_date_noted=True
                end_date = r['created_at']
                status_ctr += 1
            log.debug("Start Date: " + start_date)
            log.debug("End Date: " + end_date)
            log.debug("Ctr: " + str(status_ctr))
            sd = int(time.mktime(dateutil.parser.parse(start_date).timetuple()))
            ed = int(time.mktime(dateutil.parser.parse(end_date).timetuple()))
            delta = sd-ed
            if delta == 0:
                delta = 1
            log.debug("Delta secs.: " + str(delta))
            if status_ctr <= 1:
                status_ctr = .0000000001
            activity = 60*(float(status_ctr)/delta)
            log.debug("Activity: " + str(activity) + " tweets/minute")
        except Exception, e:
            log.debug("Error accessing: %r" % (e))
        return activity
        
    def r2a(self, user,count=count):
        reach = self.reach(user, count)
        activity = self.activity(user, count)
        log.debug("R/A: " + str(reach/activity))
        return reach/activity

    def a2r(self, user, count=count):
        reach = self.reach(user, count)
        activity = self.activity(user, count)
        log.debug("A/R: " + str(activity/reach))
        return activity/reach
