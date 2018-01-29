# -*- coding: UTF-8 -*-
from abc import ABCMeta


class Events(object):
    def __init__(self, created, code, severity, category, sourceType, sourceId):
        self.created = created  # date of creation
        self.code = code  # code
        self.severity = severity  # severity
        self.category = category  # category
        self.sourceType = sourceType  # source Type
        self.sourceId = sourceId  # source id

    def messageFromClass(self, description):  # returning event with dic in child classes
        """возврат словаря поле класса - значение и описания события"""
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
    def __init__(self, code, zcName, ccName, operaton, services, segment, operStatus, parent=None):
        super(ZCandUS, self).__init__(parent)  # init from super class with same params
        # optional params
        self.services = services
        self.operation = operaton
        self.zcName = zcName
        self.operStatus = operStatus
        self.ccName = ccName
        self.segment = segment


class TKO(ZCandUS):
    def __init__(self, code, message, errorMsg, operStatus, segment=None, unitName=None, unitType=None,
                  parent=None):
        super(TKO, self).__init__(parent)
        self.segment = segment
        self.unitName = unitName
        self.unitType = unitType
        self.message = message
        self.errorMsg = errorMsg


class OM(ZCandUS):
    def __init__(self,code, operStatus, objName, className,
                 dsName, dsType,
                 admStatus, errorMsg, parent=None):
        super(OM, self).__init__(parent)
        self.objName = objName
        self.className = className
        self.dsName = dsName
        self.dsType = dsType
        self.admStatus = admStatus
        self.errorMsg = errorMsg


class PS(ZCandUS):
    def __init__(self,code, zcName, softName, familyName,
                 operStatus,
                 admStatus, errorMsg, parent=None):
        super(PS, self).__init__(zcName, operStatus, parent)
        self.softName = softName
        self.familyName = familyName
        self.admStatus = admStatus
        self.errorMsg = errorMsg


class NetworkConnections(Events):
    def __init__(self, code,netName, parent=None):
        super(NetworkConnections, self).__init__(parent)
        self.netName = netName


class LinesAndTract(NetworkConnections):
    def __init__(self,code, lName, lType, lpFrom,
                 lpTo,
                 ccName, segment, operStatus, errorMsg, parent=None):
        super(LinesAndTract, self).__init__(parent)
        self.lName = lName
        self.lType = lType
        self.lpFrom = lpFrom
        self.lpTo = lpTo
        self.ccName = ccName
        self.segment = segment
        self.operStatus = operStatus
        self.errorMsg = errorMsg


class UsersAndRoles(Events):
    def __init__(self,code, postName, personName,
                 personStatus, message, parent=None):
        super(UsersAndRoles, self).__init__(parent)
        self.postName = postName
        self.personName = personName
        self.personStatus = personStatus
        self.message = message


class JournalOfEvents(Events):
    def __init__(self,code, parent=None):
        super(JournalOfEvents, self).__init__(parent)


class JournalOfActions(Events):
    def __init__(self,code, workGUI, personName, parent=None):
        super(JournalOfActions, self).__init__(parent)
        self.workGUI = workGUI
        self.personName = personName


class Documents(Events):
    def __init__(self,code, docName, docType, contentName,
                 actionType, email, parent=None):
        super(Documents, self).__init__(parent)
        self.docName = docName
        self.docType = docType
        self.contentName = contentName
        self.actionType = actionType
        self.email = email


class MetaData(Events):
    def __init__(self,code, metaName, taskName, message,
                 errorMsg, parent):
        super(MetaData, self).__init__(parent)
        self.metaName = metaName
        self.taskName = taskName
        self.message = message
        self.errorMsg = errorMsg




if __name__ == '__main__':
    print type(ZCandUS())
