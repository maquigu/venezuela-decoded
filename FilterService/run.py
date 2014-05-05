#!/usr/bin/python

from config import config
import logging as log
import tornado.ioloop
import tornado.web
from WebService import WebService

log.basicConfig(filename= config.name + '.log',level=log.DEBUG)

handler_urls = WebService.load_handlers(config.root_dir)

application = tornado.web.Application(handler_urls)

if __name__ == "__main__":
    application.listen(config.port)
    tornado.ioloop.IOLoop.instance().start()
