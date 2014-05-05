#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgi
import sys
from couchdb import Server
from jinja2 import Template

print "Content-Type: text/html"
print ""

arguments = cgi.FieldStorage()
if 'id' not in arguments:
    print 'id param required'
    sys.exit()
screen_name=arguments.getvalue('id')
lang=arguments.getvalue('lang')
couch = Server()
db_whos = couch['whos']
db_speeds = couch['speeds']
at_screen_name = '@' + screen_name
speeds = db_speeds.view('speeds/by_user', key=at_screen_name, limit=1, descending=True)
for s in speeds:
    latest = s.value
iam = db_whos[at_screen_name]
iam['at_screen_name'] = at_screen_name
iam['screen_name'] = screen_name
iamd = {}
for k, v in iam.iteritems():
    iamd[k] = v
person_detail_html=None
with open ('person_detail.html', "r") as myfile:
    person_detail_html=myfile.read()
template = Template(person_detail_html)
ret = template.render(iam=iamd, latest=latest, lang=lang)
print ret.encode(encoding='UTF-8',errors='strict')
sys.exit()
