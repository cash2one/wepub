#!/usr/bin/env python
# encoding: utf-8


from handlers.base import MainHandler
from handlers.app import AppHandler
from handlers.node import NodeHandler, NodeGroupHandler
from handlers.task import TaskHandler, JobHandler, RDSTaskHandler


url_patterns = [
    (r"/", MainHandler),
    (r"/app", AppHandler),
    (r"/app/(\w+)$", AppHandler),
    (r"/node", NodeHandler),
    (r"/node/(\w+)$", NodeHandler),
    (r"/nodegroup", NodeGroupHandler),
    (r"/nodegroup/(\w+)$", NodeGroupHandler),
    (r"/task$", TaskHandler),
    (r"/task/(\w+)$", TaskHandler),
    (r"/job", JobHandler),
    (r"/job/(\w+)$", JobHandler),
    (r"/taskrds$", RDSTaskHandler),
    (r"/taskrds/(\w+)$", RDSTaskHandler),
]
