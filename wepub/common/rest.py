#!/usr/bin/env python
# encoding: utf-8

import tornado.web
from tornado.escape import json_encode


class RESTfulHandler(tornado.web.RequestHandler):

    methods = ("lists", "gets", "create", "update", "delete",
               "update_collection", "delete_collection", "start")

    def __init__(self, application, request, **kwargs):
        super(RESTfulHandler, self).__init__(application, request, **kwargs)
        self.set_header('Content-Type', 'application/json; charset=UTF-8')

    def __getattr__(self, name):
        if name in self.methods and self.request.headers:
            raise tornado.web.HTTPError(500)
        else:
            raise AttributeError

    def get(self, resource_id=None):
        if resource_id is None:
            return self.lists()
        else:
            return self.gets(resource_id)

    def post(self, resource_id=None):
        if resource_id is None:
            return self.create()
        else:
            return self.start(resource_id)
            #  raise tornado.web.HTTPError(500)

    def put(self, resource_id=None):
        if resource_id is None:
            return self.update_collection()
        else:
            return self.update(resource_id)

    def delete(self, resource_id=None):
        if resource_id is None:
            return self.delete_collection()
        else:
            return self.delete(resource_id)

    def finish(self, chunk=None):
        if chunk is not None:
            chunk = json_encode(chunk)
        super(RESTfulHandler, self).finish(chunk)
