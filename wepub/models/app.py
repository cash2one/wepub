#!/usr/bin/env python
# encoding: utf-8


from .base import Model
from .base import String, RegexString


class App(Model):
    name = RegexString(pat='[_a-zA-Z]+$')
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
