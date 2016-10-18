#!/usr/bin/env python
# encoding: utf-8
import logging

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.autoreload
from tornado.options import options

from settings import settings
from wepub.urls import url_patterns


class MainApplication(tornado.web.Application):

    def __init__(self):
        logging.info("init MainApplication with settings: %s" % str(settings))
        url_patterns.append((r"/(.*)", tornado.web.StaticFileHandler,
                             dict(path=settings['static_path'])))
        tornado.web.Application.__init__(self, url_patterns, **settings)


def main():
    app = MainApplication()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
