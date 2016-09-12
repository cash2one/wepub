#!/usr/bin/env python
# encoding: utf-8

import sqlite3
from tornado.options import options

'''


'''

class SQLite(object):

    def __init__(self, db):
        self.conn = sqlite3.connect(options.sqlitedb)


class MySQL(object):
    pass

