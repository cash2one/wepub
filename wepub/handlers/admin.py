#!/usr/bin/env python
# encoding: utf-8

import tornado.web

from wepub.common import RESTfulHandler


class Job(tornado.web.RequestHandler):

    def get(self):
        self.render('job.html')


class Task(tornado.web.RequestHandler):

    def get(self):
        self.render('task.html')


class Node(tornado.web.RequestHandler):

    def get(self):
        self.render('node.html')


class NodeGroup(tornado.web.RequestHandler):

    def get(self):
        self.render('nodegroup.html')


class AppBoard(tornado.web.RequestHandler):

    def get(self):
        self.render('appboard.html')


class TaskBoard(tornado.web.RequestHandler):

    def get(self):
        self.render('taskboard.html')
