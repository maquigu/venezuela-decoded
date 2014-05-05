import traceback
import logging as log
from couchdb import Server
from tornado.web import RequestHandler
from tornado.escape import json_decode
from tornado.escape import json_encode

class SpeedTSVHandler(RequestHandler):

    db_speeds = None

    def initialize(self):
        couch = Server()
        self.db_speeds = couch['speeds']

    @staticmethod
    def url():
        return r'/speed/([^/]+)/([^/]+)\.tsv'

    def post(self):
        self.get()

    def get(self, user, amount):
        if amount == 'all':
            res = self.db_speeds.view('speeds/by_user', key=user)
        else:
            
            limit=int(amount[5:])
            res = self.db_speeds.view('speeds/by_user', key=user, limit=limit)
        ret_tsv='\ttimestamp\tactivity\treach\ta2r\tr2a\n'
        for row in res:
            r = row.value
            ret_tsv+='\t%r\t%r\t%r\t%r\t%r\n' % (r['timestamp'][0:16], r['activity'], r['reach'], r['a2r'], r['r2a'])   
        self.write(ret_tsv)
