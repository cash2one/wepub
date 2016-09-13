#!/usr/bin/env python
# encoding: utf-8

from datetime import datetime
import re
from bisect import insort

from funcsigs import Parameter, Signature

from wepub.common.db import


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


# Specialized types
class Integer(Typed):
    ty = int


class Float(Typed):
    ty = float


class String(Typed):
    ty = basestring


# Value checking
class Positive(Descriptor):
    def __set__(self, instance, value):
        if value < 0:
            raise ValueError('Expected >= 0')
        super(Positive, self).__set__(instance, value)


# More specialized types
class PosInteger(Integer, Positive):
    pass


class PosFloat(Float, Positive):
    pass


# Length checking
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


# Pattern matching
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

# Model definition code


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

    def __init__(self, *args, **kwargs):
        bound = self.__signature__.bind(*args, **kwargs)
        for name, val in bound.arguments.items():
            setattr(self, name, val)
        self.timestamp = datetime.utcnow()

    def valid_data(self):
        raise NotImplementedError("Must Implement `valid_data` method")

    def save(self):
        pass

if __name__ == '__main__':
    class Stock(Model):
        name = SizedRegexString(maxlen=8, pat='[A-Z]+$')
        shares = PosInteger()
        price = PosFloat()

    s = Stock("APPLE", 5504, 105.44)
    print(s.name)
    print(s.shares)
    print(s.price)
