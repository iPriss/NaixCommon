# -*- coding: utf-8 -*-
from NaixCommon import simplejson
from exceptions import Exception

class Serializable:
    def __init__(self, **kwargs):
        if len(kwargs) == 1 and type(kwargs[kwargs.keys()[0]]) is dict:
            # FIXME: if this if is entered to, it blows up. kwargs doesn't have an elem[0].
            # Also, use kwargs.values[0], more concise.
            self.fromDict(kwargs[0])
        elif len(kwargs) > 0:
            self.fromDict(kwargs)

    def fromDict(self, daDict):
        for key in self.__dict__:
            if not key in daDict.keys():
                raise InsuficientDictionaryError, "%s object require '%s' attribute, but the given dictionary does not provide it." % (self.__class__, key)

        self.__dict__ = daDict

    def getAttrList(self):
        tmp = self.__dict__.keys()
        quitList = ['__doc__', '__init__', '__module__']
        for i in quitList:
            if i in tmp:
                tmp.remove(i)
        return tmp

    def __repr__(self):
        return str(self.__dict__)

    def __setitem__(self, key, item):
        setattr(self, key, item)

    def serialize(self, form='JSON'):
        tmp = {}
        tmp = self.__dict__
#        for k, v in self.__dict__:
#            if k[0] <> '_':
#                tmp[k] = v

        return simplejson.dumps(tmp, use_decimal=True)

    def getSerializableDict(self):
        return self.__dict__


class InsuficientDictionaryError(Exception):
    """
    exception throwned when a dictionary has not enought items
    to fill a Value Object
    """
    pass

