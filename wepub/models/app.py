#!/usr/bin/env python
# encoding: utf-8


from .base import Model
from .base import Float, Integer, String, RegexString


class App(Model):
    _id = Integer()
    name = RegexString(pat='[_a-zA-Z]+$')
    cname = String()
    version = String()
    platform = String()
    packagesource = String()
    administrator = String()

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
