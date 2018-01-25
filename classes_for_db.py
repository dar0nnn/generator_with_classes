# -*- coding: UTF-8 -*-
from abc import ABCMeta


class Events:
    __metaclass__ = ABCMeta

    def __init__(self, created, code, severity, category, sourceType, sourceId):
        self.created = created  # date of creation
        self.code = code  # code
        self.severity = severity  # severity
        self.category = category  # category
        self.sourceType = sourceType  # source Type
        self.sourceId = sourceId  # source id

    def messageFromClass(self, description):  # returning event with dic in child classes
        attrsNamesList = ['created', 'code', 'category', 'sourceType', 'sourceId', 'severity']
        vars = [x for x in dir(self) if
                not x.startswith('_') and x != 'messageFromClass']  # getting all vars of class to dic
        var_dict = {}
        params_dict = {}
        for var in vars:  # cycle for params to get them to db
            if getattr(self, var) is None:  # check for unnecessary vars
                continue
            else:
                if var not in attrsNamesList:
                    params_dict[var] = getattr(self, var)
                else:
                    var_dict[var] = getattr(self, var)  # filling dic with needed vars of this event
        var_dict['params'] = params_dict
        var_dict['description'] = description
        return var_dict


class ZCandUS(Events):
    def __init__(self, zcName=None, operaton=None, services=None, operStatus=None, *args, **kw):
        super(ZCandUS, self).__init__(*args, **kw)  # init from super class with same params
        # optional params
        self.services = services
        self.operation = operaton
        self.zcName = zcName
        self.operStatus = operStatus


class TKO(ZCandUS):
    def __init__(self, zcName, segment, unitName, unitType,
                 operStatus=None,
                 message=None, errorMsg=None, *args, **kw):
        super(TKO, self).__init__(zcName, operStatus, *args, **kw)
        self.segment = segment
        self.unitName = unitName
        self.unitType = unitType
        self.message = message
        self.errorMsg = errorMsg


class OM(ZCandUS):
    def __init__(self, objName=None, className=None,
                 dsName=None, dsType=None,
                 admStatus=None, errorMsg=None, *args, **kw):
        super(OM, self).__init__(*args, **kw)
        self.objName = objName
        self.className = className
        self.dsName = dsName
        self.dsType = dsType
        self.admStatus = admStatus
        self.errorMsg = errorMsg


class PS(ZCandUS):
    def __init__(self, zcName, softName, familyName,
                 operStatus=None,
                 admStatus=None, errorMsg=None, *args, **kw):
        super(PS, self).__init__(zcName, operStatus, *args, **kw)
        self.softName = softName
        self.familyName = familyName
        self.admStatus = admStatus
        self.errorMsg = errorMsg


class NetworkConnections(Events):
    def __init__(self, netName, *args, **kw):
        super(NetworkConnections, self).__init__(*args, **kw)
        self.netName = netName


class LinesAndTract(NetworkConnections):
    def __init__(self, netName, lName, lType, ipFrom=None,
                 ipTo=None,
                 ccName=None, segment=None, operStatus=None, errorMsg=None, *args, **kw):
        super(LinesAndTract, self).__init__(netName, *args, **kw)
        self.lName = lName
        self.lType = lType
        self.ipFrom = ipFrom
        self.ipTo = ipTo
        self.ccName = ccName
        self.segment = segment
        self.operStatus = operStatus
        self.errorMsg = errorMsg


class UsersAndRoles(Events):
    def __init__(self, postName=None, personName=None,
                 personStatus=None, message=None, *args, **kw):
        super(UsersAndRoles, self).__init__(*args, **kw)
        self.postName = postName
        self.personName = personName
        self.personStatus = personStatus
        self.message = message


class JournalOfEvents(Events):
    def __init__(self, *args, **kw):
        super(JournalOfEvents, self).__init__(*args, **kw)


class JournalOfActions(Events):
    def __init__(self, workGUI=None, personName=None, *args, **kw):
        super(JournalOfActions, self).__init__(*args, **kw)
        self.workGUI = workGUI
        self.personName = personName


class Documents(Events):
    def __init__(self, docName, docType, contentName=None,
                 actionType=None, email=None, *args, **kw):
        super(Documents, self).__init__(*args, **kw)
        self.docName = docName
        self.docType = docType
        self.contentName = contentName
        self.actionType = actionType
        self.email = email


class MetaData(Events):
    def __init__(self, metaName, taskName=None, message=None,
                 errorMsg=None, *args, **kw):
        super(MetaData, self).__init__(*args, **kw)
        self.metaName = metaName
        self.taskName = taskName
        self.message = message
        self.errorMsg = errorMsg


if __name__ == '__main__':
    pass
