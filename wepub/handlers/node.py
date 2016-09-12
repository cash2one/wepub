#!/usr/bin/env python
# encoding: utf-8


from wepub.common import RESTfulHandler


class NodeHandler(RESTfulHandler):
    def gets(self, node_id):
        self.finish([1, 2, 3])

    def lists(self):
        self.finish("you get all nodes")

    def create(self):
        self.finish({'method': 'create',
                     'discription': 'create resource with given arguments',
                     'arguments': self.request.arguments})


class NodeGroupHandler(RESTfulHandler):
    pass
