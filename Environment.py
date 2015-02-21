# -*- coding: utf-8 -*-
import uuid
from threading import Lock  

class Environment(object):

    _instance = None
    _mutex = Lock()

    def __new__(cls, *args, **kwargs):
        with cls._mutex:
            if not cls._instance:
                try:
                    cls._instance = super(Environment, cls).__new__(cls, *args, **kwargs)
                    cls._instance.reset()
                except:
                    cls._instance = None
                    raise
        return cls._instance

    def __getitem__(self, key):
        return self.attributes[key]

    def __setitem__(self, key, value):
        self.attributes[key] = value

    def reset(self):
        self.attributes = {
            'correlationId': str(uuid.uuid4())
        }