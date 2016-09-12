#!/usr/bin/env python
# encoding: utf-8

from common.db import SQLite


class App(object):

    fields = ('name', 'cname', 'version', 'platform',
              'packagesource', 'administrator')

    def __init__(self, name, cname, version, platform,
                 packagesource, administrator, **kwargs):
        self.name = name
        self.cname = cname
        self.version = version
        self.platform = platform
        self.packagesource = packagesource
        self.administrator = administrator

    @property
    def valid_data(self):
        data = {}
        __ = vars(self)
        for field in self.fields:
            data[field] = __.get(field)
        return data

    #  def serialize(self):
        #  s = json.dumps(self, default=self.valid_data)
        #  return s

    @staticmethod
    def unserialize(dct):
        obj = App.__new__(App)
        for k, v in dct.iteritems():
            if k in App.fields:
                setattr(obj, k, v)
        return obj

    def create(self):
        db.app_table.save(self.data)
