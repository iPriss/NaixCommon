# -*- coding: utf-8 -*-
from NaixCommon import simplejson
from BaseClasses import Serializable
import uuid

class VO_Message(Serializable, BaseException):
    def __init__(self, description, status, code, traceback=None, **kwargs):
        self.description = description
        self.status = status
        self.code = code
        self.traceback = traceback
        self.errorCode = str(uuid.uuid4())

        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def getSerializableDict(self):
        return dict(((k, val) for k, val in self.__dict__.iteritems() if k[0] != '_'))

    class statuses:
        ERROR = "ERROR"
        INFO = "INFO"
        SERVER_ERROR = "SERVER_ERROR"

    def __str__(self):
        attrs = ['description', 'code', 'status', 'traceback']
        attrs += [k for k in self.__dict__ if k not in attrs]
        return ', '.join([str(getattr(self, i)) for i in attrs])

    def __repr__(self):
        return str(self)