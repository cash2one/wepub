#!/usr/bin/env python
# encoding: utf-8

from .base import Model
from .base import Float, Integer, String, RegexString


class Node(Model):
    hostname = String()
    category = RegexString(pat=r'(\bcontainer\b)|(\bphysical\b)')
    clustername = RegexString(pat=r'[-_a-zA-Z]+$')
    clusterid = String()
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


class NodeGroup(Model):
    name = RegexString(pat=r'[-0-9_a-zA-Z]+$')
    cname = String()
    category = String()
    nodes = String()

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
