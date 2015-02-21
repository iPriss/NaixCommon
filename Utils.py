# -*- coding: utf-8 -*-
import time
import pickle
import inspect

from copy import deepcopy
from decimal import Decimal
from datetime import datetime
from binascii import unhexlify as unhex
from binascii import hexlify as dohex
# from modules.pyDes import *

from NaixCommon.ValueObjects import Serializable, VO_Message
from NaixCommon import simplejson

import config

def getParam(di, key, defaultValue):
    """
    given a dictionary di returns the value of key.
    if key is not in di, returns defaultValue
    """
    if type(di) is dict:
        if key in di:
            return di[key]
        else:
            return defaultValue
    else:
        if hasattr(di,key):
            return getattr(di,key)
        else:
            return defaultValue

def query(sql, *args, **kwargs):
   eng = create_engine('postgresql://lega-user:lega2011/lega')
   con = eng.connect()
   return con.execute(sql, *args, **kwargs)
   #aca hay que ver si devuelve un cursor o que y devolver la data en un diccionario o lista nomas.            

def JSONEncode(data):
    return simplejson.dumps(data, use_decimal=True)

def currentTimestamp():
    return "%04d%02d%02dT%02d%02d%02dZ" % tuple(time.gmtime())[:6:]

class InParams:
    def __init__(self, *inParams):
        self.inParams = inParams

    def __getitem__(self,name):
        for param in self.inParams:
            if name == param.name: return param

class InParam:
    def __init__(self, name, mandatory, dataType, onlyValues=None, between=None):
        self.name = name
        self.mandatory = mandatory
        self.dataType = dataType
        self.onlyValues = onlyValues
        self.between = between    

def Validate(inParams, paramsGet):
    """
    inParams is InParams instance
    paramsGet a dict

    This function matches the inParams and paramsGet looking for diferences
    """
    Errors = []

    pars = {}

    #see if any mandatory key is missing
    for key in [i.name for i in inParams.inParams if i.mandatory]:
        if key not in paramsGet:
            Errors.append(VO_Message("%s required" % str(key), 'ERROR', 108))

    #see if are exeding keys
    for key in paramsGet.keys():
        if key not in [i.name for i in inParams.inParams]:
            Errors.append(VO_Message("invalid parameter %s" % str(key), 'ERROR', 109))

    #data type
    #for mandatory
    for inParam in [inPara for inPara in inParams.inParams if inPara.mandatory]:
        try:
            pars[inParam.name] = inParam.dataType(paramsGet[inParam.name])
        except:
            Errors.append(VO_Message("%s parameter is not type %s" % (str(inParam.name),str(inParam.dataType)), 'ERROR', 107))

    #for existing non mandatory
    for inParam in [inPara for inPara in inParams.inParams if not inPara.mandatory and inPara.name in paramsGet.keys()]:
        try:
            pars[inParam.name] = inParam.dataType(paramsGet[inParam.name])
        except:
            Errors.append(VO_Message("%s parameter is not type %s" % (str(inParam.name),str(inParam.dataType)), 'ERROR', 107))

    if Errors:
        raise Errors[0]

    #data set
    for key, item in pars.iteritems():
        if inParams[key].onlyValues:
            if inParams[key].dataType == Decimal:
                if not eval(inParams[key].onlyValues, {'X':inParams[key].dataType(item)}):
                    Errors.append(VO_Message("%s parameter must comply with condition %s" % (key,str(inParams[key].onlyValues)), 'ERROR', 107))
            else:
                if inParams[key].dataType(item) not in inParams[key].onlyValues:
                    Errors.append(VO_Message("%s parameter must be among this values %s" % (key,str(inParams[key].onlyValues)), 'ERROR', 107))

    for key, item in pars.iteritems():
        if inParams[key].between:
            val = inParams[key].dataType(item)
            if not (val >= inParams[key].between[0] and val <= inParams[key].between[1]):
                Errors.append(VO_Message("%s parameter must be between this values %s" % (key,str(inParams[key].between)), 'ERROR', 107))

    if Errors:
        raise Errors[0]

    #adding non-existing non mandatory
    for inParam in [inPara for inPara in inParams.inParams if not inPara.mandatory and inPara.name not in paramsGet.keys()]:
        pars[inParam.name] = None


    return pars


MANDATORY = True
OPTIONAL = False