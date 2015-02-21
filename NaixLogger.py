# -*- coding: utf-8 -*-
import sys
import logging
from NaixCommon.Environment import Environment

class NaixLogger(object):

    logFormat = '[%(asctime)-15s] [%(correlationId)s] %(message)s'
    enabled = True

    class LogFilter(logging.Filter):
        def filter(self, record):
            if record.args:
                record.msg = record.msg % record.args
                record.args = tuple()
            record.msg = record.msg.replace('\n', '\\n').replace('\r', '\\r')
            record.correlationId = Environment()['correlationId']
            return NaixLogger.enabled

    sys.stderr = sys.stdout
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(logFormat))
    handler.addFilter(LogFilter())
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger('suds').setLevel(logging.INFO)


    def __new__(cls, *args, **kwargs):
        return logging.getLogger()