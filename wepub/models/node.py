#!/usr/bin/env python
# encoding: utf-8

from .base import Model
from .base import Float, Integer, String, RegexString


class Node(Model):
    _id = Integer()
    clastername = RegexString(pat='[a-zA-Z]+$')
    clasterid = String()
    nodename = String()
    saltid = String()
    ipaddr = String()
    category = String()

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


class NodeGroup(Model):
    _id = Integer()
    clastername = RegexString(pat='[a-zA-Z]+$')
    clasterid = String()
    nodename = String()
    saltid = String()
    ipaddr = String()

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
