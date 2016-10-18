#!/usr/bin/env python
# encoding: utf-8

import sqlite3
from tornado.options import options


class MySQL(object):
    pass


queries = {
    'SELECT': 'SELECT %s FROM %s WHERE %s',
    'SELECT_ALL': 'SELECT %s FROM %s',
    'INSERT': 'INSERT OR REPLACE INTO %s VALUES(%s)',
    'UPDATE': 'UPDATE %s SET %s WHERE %s',
    'DELETE': 'DELETE FROM %s where %s',
    'DELETE_ALL': 'DELETE FROM %s',
    'CREATE_TABLE': 'CREATE TABLE IF NOT EXISTS %s(%s)',
    'DROP_TABLE': 'DROP TABLE %s'
}


class SQLite(object):

    def __init__(self):
        self.data_file = options.sqlitedb
        self.db = sqlite3.connect(self.data_file, check_same_thread=False)

    def close(self, cursor=None):
        if cursor:
            cursor.close()
        else:
            self.db.cursor.close()

    def write(self, query, values=None):
        cursor = self.db.cursor()
        if values is not None:
            cursor.execute(query, list(values))
        else:
            cursor.execute(query)
        self.db.commit()
        return cursor

    def read(self, query, values=None):
        cursor = self.db.cursor()
        if values is not None:
            cursor.execute(query, list(values))
        else:
            cursor.execute(query)
        return cursor

    def select(self, tables, *args, **kwargs):
        vals = ','.join([l for l in args])
        locs = ','.join(tables)
        conds = ' and '.join(['%s=?' % k for k in kwargs])
        subs = [kwargs[k] for k in kwargs]
        query = queries['SELECT'] % (vals, locs, conds)
        return self.read(query, subs)

    def select_all(self, tables, *args):
        vals = ','.join([l for l in args])
        locs = ','.join(tables)
        query = queries['SELECT_ALL'] % (vals, locs)
        return self.read(query)

    def insert(self, table_name, *args):
        values = ','.join(['?' for l in args])
        query = queries['INSERT'] % (table_name, values)
        return self.write(query, args)

    def update(self, table_name, set_args, **kwargs):
        updates = ','.join(['%s=?' % k for k in set_args])
        conds = ' and '.join(['%s=?' % k for k in kwargs])
        vals = [set_args[k] for k in set_args]
        subs = [kwargs[k] for k in kwargs]
        query = queries['UPDATE'] % (table_name, updates, conds)
        return self.write(query, vals + subs)

    def delete(self, table_name, **kwargs):
        conds = ' and '.join(['%s=?' % k for k in kwargs])
        subs = [kwargs[k] for k in kwargs]
        query = queries['DELETE'] % (table_name, conds)
        return self.write(query, subs)

    def delete_all(self, table_name):
        query = queries['DELETE_ALL'] % table_name
        return self.write(query)

    def create_table(self, table_name, values):
        query = queries['CREATE_TABLE'] % (table_name, ','.join(values))
        self.close(self.write(query))

    def drop_table(self, table_name):
        query = queries['DROP_TABLE'] % table_name
        self.close(self.write(query))


if __name__ == '__main__':
    apptable = SQLite().drop_table('app')
