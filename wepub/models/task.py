#!/usr/bin/env python
# encoding: utf-8

from .base import Model
from .base import Float, Integer, String, RegexString


class Task(Model):
    _id = Integer()
    name = String()
    appid = String()
    nodes = String()
    nodes_success = String()
    nodes_failed = String()
    jobs = String()
    status = RegexString(pat='(\bwaiting\b)|(\bexecuting\b) \
                             |(\bstopped\b)|(\bcompleted\b) \
                             |(\bsuspend\b)')
    creator = String()
    starttime = String()
    endtime = String()

    @property
    def valid_data(self):
        data = {}
        _ = vars(self)
        for key, val in _.items():
            # valid every field here
            data[key] = val
        return data

    def create(self):
        self.save(self.valid_data)


class Job(Model):
    _id = Integer()
    name = String()
    status = RegexString(pat='(\bwaiting\b)|(\bexecuting\b) \
                             |(\bstopped\b)|(\bcompleted\b) \
                             |(\bsuspend\b)')
    category = String()
    content = String()

    @property
    def valid_data(self):
        data = {}
        _ = vars(self)
        for key, val in _.items():
            # valid every field here
            data[key] = val
        return data

    def create(self):
        self.save(self.valid_data)
