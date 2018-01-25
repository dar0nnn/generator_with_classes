# -*- coding: UTF-8 -*-
from abc import ABCMeta, abstractmethod


# abstract Event
class Events:
    __metaclass__ = ABCMeta

    def __init__(self, created, code, severity, category, sourceType, sourceId):
        self.created = created  # date of creation
        self.code = code  # code
        self.severity = severity  # severity
        self.category = category  # category
        self.sourceType = sourceType  # source Type
        self.sourceId = sourceId  # source id

    @abstractmethod
    def message(self):  # returning event with dic in child classes
        pass


class Infrastructure(Events):
    def message(self):  # returning event with dic in child classes
        vars = [x for x in dir(self) if not x.startswith('_') and x != 'message']  # getting all vars of class to dic
        var_dict = {}
        for var in vars:  # cycle for params to get them to db
            if getattr(self, var) is None:  # check for unnecessary vars
                continue
            else:
                var_dict[var] = getattr(self, var)  # filling dic with needed vars of this event
        return var_dict


class ZCandUS(Infrastructure):
    def __init__(self, created, code, severity, category, sourceType,
                 sourceId, zcName, operaton=None, services=None, operStatus=None):
        super(ZCandUS, self).__init__(created, code, severity, category, sourceType,
                                      sourceId)  # init from super class with same params
        # optional params
        self.services = services
        self.operation = operaton
        self.zcName = zcName
        self.operStatus = operStatus


class TKO(ZCandUS):
    def __init__(self, created, code, severity, category, sourceType, sourceId, zcName, segment, unitName, unitType, operStatus = None,
                 message=None, errorMsg=None):
        super(TKO, self).__init__(created, code, severity,category, sourceType, sourceId, zcName, operStatus)
        self.segment = segment
        self.unitName = unitName
        self.unitType = unitType
        self.msg = message
        self.errorMsg = errorMsg


class OM(ZCandUS):
    def __init__(self, created, code, severity, category, sourceType, sourceId, zcName, objName=None, className=None,
                 dsName=None, dsType=None,
                 operStatus=None, admStatus=None, errorMsg=None):
        super(OM, self).__init__(created, code, severity, category, sourceType, sourceId, zcName, operStatus)
        self.objName = objName
        self.className = className
        self.dsName = dsName
        self.dsType = dsType
        self.admStatus = admStatus
        self.errorMsg = errorMsg


class PS(ZCandUS):
    def __init__(self, created, code, severity, category, sourceType, sourceId, zcName, softName, familyName,
                 operStatus=None,
                 admStatus=None, errorMsg=None):
        super(PS, self).__init__(created, code, severity, category, sourceType, sourceId, zcName, operStatus)
        self.softName = softName
        self.familyName = familyName
        self.admStatus = admStatus
        self.errorMsg = errorMsg


if __name__ == '__main__':
    zcname = ZCandUS('created', 'code', 'severity', 'category', 'sourceType', 'sourceId', zcName='zcName')
    ucname = ZCandUS('created', 'code', 'severity', 'category', 'sourceType', 'sourceId', zcName='zcName',
                     operStatus='operstatus')
    change = ZCandUS('created', 'code', 'severity', 'category', 'sourceType', 'sourceId', 'operation',
                     'services', 'segmentZCName')
    ps = PS('created', 'code', 'severity', 'category', 'sourceType', 'sourceId', 'zcName','softname', 'familyname', errorMsg='hi')
    om = OM('created', 'code', 'severity', 'category', 'sourceType', 'sourceId', zcName='zcName', operStatus='status')
    tko_dict = {}
    try:
        tko = TKO('created', 'code', 'severity', 'category', 'sourceType', 'sourceId', 'zcName', 'segmentname', 'unitname', 'unittype')
        tko_dict = tko.message()
    except Exception as e:
        print e
    print zcname.message()
    print ucname.message()
    print change.message()
    print ps.message()
    print om.message()