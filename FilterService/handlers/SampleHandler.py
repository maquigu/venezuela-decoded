import traceback
import logging as log
from tornado.web import RequestHandler
from tornado.escape import json_decode
from tornado.escape import json_encode

class SampleHandler(RequestHandler):

    db_users = None

    def initialize(self):
        pass # DB init, etc.

    @staticmethod
    def url():
        return r'/sample'

    def post(self):
        self.get()

    def get(self):
        self.write('Hello, World!')
