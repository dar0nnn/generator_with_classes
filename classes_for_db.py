# -*- coding: UTF-8 -*-
from abc import ABCMeta


class Events(object):
    def __init__(self, code, created=None, severity=None, category=None, sourceType=None, sourceId=None):
        self.created = created  # date of creation
        self.code = code  # code
        self.severity = severity  # severity
        self.category = category  # category
        self.sourceType = sourceType  # source Type
        self.sourceId = sourceId  # source id

    def messageFromClass(self, description):  # returning event with dic in child classes
        """возврат словаря поле класса - значение и описания события"""
        attrsNamesList = [u'created', u'code', u'category', u'sourceType', u'sourceId', u'severity']
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
        var_dict[u'params'] = params_dict
        var_dict[u'description'] = description
        return var_dict


class ZCandUS(Events):
    def __init__(self, code, zcName=None, ccName=None, operaton=None, services=None, operStatus=None, parent=None):
        super(ZCandUS, self).__init__(parent)  # init from super class with same params
        # optional params
        self.services = services
        self.operation = operaton
        self.zcName = zcName
        self.operStatus = operStatus
        self.ccName = ccName
        self.code = code

class TKO(ZCandUS):
    def __init__(self, code, segment=None, unitName=None, unitType=None,
                 message=None, errorMsg=None, parent=None):
        super(TKO, self).__init__(parent)
        self.segment = segment
        self.unitName = unitName
        self.unitType = unitType
        self.message = message
        self.errorMsg = errorMsg
        self.code = code

class OM(ZCandUS):
    def __init__(self, code, objName=None, className=None,
                 dsName=None, dsType=None,
                 admStatus=None, errorMsg=None, parent=None):
        super(OM, self).__init__(parent)
        self.objName = objName
        self.className = className
        self.dsName = dsName
        self.dsType = dsType
        self.admStatus = admStatus
        self.errorMsg = errorMsg
        self.code = code

class PS(ZCandUS):
    def __init__(self, code, zcName=None, softName=None, familyName=None,
                 operStatus=None,
                 admStatus=None, errorMsg=None, parent=None):
        super(PS, self).__init__(zcName, operStatus, parent)
        self.softName = softName
        self.familyName = familyName
        self.admStatus = admStatus
        self.errorMsg = errorMsg
        self.code = code

class NetworkConnections(Events):
    def __init__(self, code, netName=None, parent=None):
        super(NetworkConnections, self).__init__(parent)
        self.netName = netName
        self.code = code

class LinesAndTract(NetworkConnections):
    def __init__(self, code, lName=None, lType=None, lpFrom=None,
                 lpTo=None,
                 ccName=None, segment=None, operStatus=None, errorMsg=None, parent=None):
        super(LinesAndTract, self).__init__(parent)
        self.lName = lName
        self.lType = lType
        self.lpFrom = lpFrom
        self.lpTo = lpTo
        self.ccName = ccName
        self.segment = segment
        self.operStatus = operStatus
        self.errorMsg = errorMsg
        self.code = code

class UsersAndRoles(Events):
    def __init__(self, code, postName=None, personName=None,
                 personStatus=None, message=None, parent=None):
        super(UsersAndRoles, self).__init__(parent)
        self.postName = postName
        self.personName = personName
        self.personStatus = personStatus
        self.message = message
        self.code = code

class JournalOfEvents(Events):
    def __init__(self, code, parent=None):
        super(JournalOfEvents, self).__init__(parent)
        self.code = code

class JournalOfActions(Events):
    def __init__(self, code, workGUI=None, personName=None, parent=None):
        super(JournalOfActions, self).__init__(parent)
        self.workGUI = workGUI
        self.personName = personName
        self.code = code

class Documents(Events):
    def __init__(self, code, docName=None, docType=None, contentName=None,
                 actionType=None, email=None, parent=None):
        super(Documents, self).__init__(parent)
        self.docName = docName
        self.docType = docType
        self.contentName = contentName
        self.actionType = actionType
        self.email = email
        self.code = code

class MetaData(Events):
    def __init__(self, code, metaName=None, taskName=None, message=None,
                 errorMsg=None, parent=None):
        super(MetaData, self).__init__(parent)
        self.metaName = metaName
        self.taskName = taskName
        self.message = message
        self.errorMsg = errorMsg
        self.code = code

if __name__ == '__main__':
    print type(ZCandUS())
