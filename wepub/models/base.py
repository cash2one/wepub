#!/usr/bin/env python
# encoding: utf-8

from datetime import datetime
import re
from bisect import insort
import hashlib

from funcsigs import Parameter, Signature
from wepub.common.db import SQLite


class Descriptor(object):
    __counter = 0

    def __init__(self, name=None):
        self.name = name
        self.__counter = Descriptor.__counter
        Descriptor.__counter += 1

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        raise AttributeError("Can't delete")

    def __cmp__(self, other):
        return cmp(self.__counter, other.__counter)


class Typed(Descriptor):
    ty = object

    def __set__(self, instance, value):
        if not isinstance(value, self.ty):
            raise TypeError('Expected %s' % self.ty)
        super(Typed, self).__set__(instance, value)


class Integer(Typed):
    ty = int


class Float(Typed):
    ty = float


class String(Typed):
    ty = basestring


class Positive(Descriptor):
    def __set__(self, instance, value):
        if value < 0:
            raise ValueError('Expected >= 0')
        super(Positive, self).__set__(instance, value)


class PosInteger(Integer, Positive):
    pass


class PosFloat(Float, Positive):
    pass


class Sized(Descriptor):

    def __init__(self, *args, **kwargs):
        self.maxlen = kwargs.pop('maxlen')
        super(Sized, self).__init__(*args, **kwargs)

    def __set__(self, instance, value):
        if len(value) > self.maxlen:
            raise ValueError('Too big')
        super(Sized, self).__set__(instance, value)


class SizedString(Sized, String):
    pass


class Regex(Descriptor):
    def __init__(self, *args, **kwargs):
        self.pat = re.compile(kwargs.pop('pat'))
        super(Regex, self).__init__(*args, **kwargs)

    def __set__(self, instance, value):
        if not self.pat.match(value):
            raise ValueError('Invalid string, must comply with'
                             'regex %s' % self.pat.pattern)
        super(Regex, self).__set__(instance, value)


class SizedRegexString(SizedString, Regex):
    pass


class RegexString(String, Regex):
    pass


def make_signature(names):
    return Signature(
        Parameter(name, Parameter.POSITIONAL_OR_KEYWORD)
        for name in names)


class ModelMeta(type):

    def __new__(cls, clsname, bases, clsdict):
        _fields = []
        for key, val in clsdict.items():
            if isinstance(val, Descriptor):
                val.name = key
                insort(_fields, val)
        fields = [x.name for x in _fields]
        clsobj = super(ModelMeta, cls).__new__(cls, clsname, bases, clsdict)
        sig = make_signature(fields)
        setattr(clsobj, '__signature__', sig)
        return clsobj


class Model(object):
    __metaclass__ = ModelMeta
    __db__ = SQLite()

    def __init__(self, *args, **kwargs):
        bound = self.__signature__.bind(*args, **kwargs)
        for name, val in bound.arguments.items():
            setattr(self, name, val)
        _ = ''.join(sorted(map(str, self.__dict__.values())))
        self._id = hashlib.md5(_).hexdigest()[:16]
        self.timestamp = str(datetime.utcnow())
        self._create_table()
        self.save()

    @property
    def tablename(self):
        return self.__class__.__name__.lower()

    def _create_table(self):
        type_mapping = {None: 'NULL', int: 'INTEGER', long: 'INTEGER',
                        float: 'REAL', str: 'TEXT', unicode: 'TEXT',
                        buffer: 'BLOB'}
        tablecond = []
        for field, value in sorted(self.__dict__.items()):
            fieldcond = "{0} {1}".format(field, type_mapping[type(value)])
            if field == '_id':
                fieldcond = fieldcond + ' UNIQUE PRIMARY KEY'
            tablecond.append(fieldcond)
        self.__db__.create_table(self.tablename, tablecond)

    def valid_data(self):
        raise NotImplementedError("Must Implement `valid_data` method")

    def save(self):
        _ = sorted(self.__dict__.items())
        data = [v for k, v in _]
        self.__db__.insert(self.tablename, *data)

    @classmethod
    def all_data(cls):
        tablename = cls.__name__.lower()
        cur = cls.__db__.select_all([tablename], '*')
        ret = cur.fetchall()
        cur.close()
        return ret

    @classmethod
    def get_object_by_id(cls, _id=None):
        pass

    @classmethod
    def get_data_by_id(cls, _id=None):
        tablename = cls.__name__.lower()
        if _id is not None:
            cur = cls.__db__.select([tablename], '*', _id=_id)
            ret = cur.fetchone()
            cur.close()
            return ret

    @classmethod
    def update_table(cls, set_args, conds):
        tablename = cls.__name__.lower()
        cur = cls.__db__.update([tablename], '*', set_args, conds)
        return cur


if __name__ == '__main__':
    class Stock(Model):
        name = SizedRegexString(maxlen=8, pat='[A-Z]+$')
        shares = PosInteger()
        price = PosFloat()

    s = Stock(u"APPLE", 5504, 105.44)
    s2 = Stock("APPLE", 5504, 105.44)
    s3 = Stock("APP", 504, 10.44)
    #  print Stock.get_data_by_id(_id='f5749a978db0ab34')
    print Stock.all_data()
    #  print(s._id)
    #  print(s.name)
    #  print(s.shares)
    #  print(s.price)
    #  print(s.timestamp)
