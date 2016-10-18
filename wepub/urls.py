#!/usr/bin/env python
# encoding: utf-8

from handlers import admin
from handlers.base import MainHandler
from handlers.app import AppHandler
from handlers.node import NodeHandler, NodeGroupHandler
from handlers.task import TaskHandler, JobHandler, RDSTaskHandler


# RESTful API for this system
url_patterns = [
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

# Handlers for Web Admin interface
url_patterns += [
    (r"/", MainHandler),
    (r"/admin", MainHandler),
    (r"/admin/job", admin.Job),
    (r"/admin/task", admin.Task),
    (r"/admin/node", admin.Node),
    (r"/admin/nodegroup", admin.NodeGroup),
    (r"/admin/appboard", admin.AppBoard),
    (r"/admin/taskboard", admin.TaskBoard),
]
