# -*- coding: utf-8 -*-
from ValueObjects import VO_Message

class INVALID_LICENSE(VO_Message):
    def __init__(self, traceback=None):
        VO_Message.__init__(self, 'Invalid license', VO_Message.statuses.ERROR, 102, traceback)

class INVALID_GAME(VO_Message):
    def __init__(self, traceback=None):
        VO_Message.__init__(self, 'Invalid game', VO_Message.statuses.ERROR, 103, traceback)

class INVALID_CASINO_OPERATOR(VO_Message):
    def __init__(self, traceback=None):
        VO_Message.__init__(self, 'Invalid casino operator', VO_Message.statuses.ERROR, 104, traceback)

class INVALID_USER_IDENTIFIER(VO_Message):
    def __init__(self, traceback=None):
        VO_Message.__init__(self, 'Invalid user identifier', VO_Message.statuses.ERROR, 106, traceback)

class BAD_REQUEST(VO_Message):
    def __init__(self, traceback=None):
        VO_Message.__init__(self, 'Invalid or Malformed Request', VO_Message.statuses.ERROR, 107, traceback)

class INTERNAL_SERVER_ERROR(VO_Message):
    def __init__(self, description='Internal server error', status=VO_Message.statuses.ERROR, code=107, traceback=None, **kwargs):
        VO_Message.__init__(self, description, status, code, traceback, **kwargs)

class EXPIRED_LICENSE(VO_Message):
    def __init__(self, traceback=None):
        VO_Message.__init__(self, 'Expired License', VO_Message.statuses.ERROR, 110, traceback)

class INVALID_CURRENCY(VO_Message):
    def __init__(self, currencyId, traceback=None):
        VO_Message.__init__(self, 'Invalid currency (%s)' % currencyId, VO_Message.statuses.ERROR, 111, traceback)

class MAINTENANCE_MODE(VO_Message):
    def __init__(self, traceback=None):
        VO_Message.__init__(self, 'Service under maintenance. Please come back later', VO_Message.statuses.ERROR, 112, traceback)