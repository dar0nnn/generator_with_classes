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
    def __init__(self, zcName=None, ccName=None, operaton=None, services=None, operStatus=None, *args, **kw):
        super(ZCandUS, self).__init__(*args, **kw)  # init from super class with same params
        # optional params
        self.services = services
        self.operation = operaton
        self.zcName = zcName
        self.operStatus = operStatus
        self.ccName = ccName


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


# объявления классов шаблонов, для спцефических событий
addseg_oper_status_changed = ZCandUS(code=u'1.1.1.10', operStatus=None)
cc_service = ZCandUS(code=u'1.1.1.9', segment=None, services=None, operaton=None)
tko_changed = TKO(code=u'1.1.1.5.3', message=None)
tko_oper_status_changed = TKO(code=u'1.1.1.5.5', operStatus=None, errorMsg=None)
ds_oper_status_changed = OM(code=u'1.1.1.6.12', dsName=None, dsType=None, operStatus=None, errorMsg=None)
obj_adm_status_changed = OM(code=u'1.1.1.6.11', objName=None, className=None, admStatus=None)
soft_adm_status_changed = PS(code=u'1.1.1.7.1.8', softName=None, familyName=None, admStatus=None)
soft_oper_status_changed = PS(code=u'1.1.1.7.1.7', softName=None, familyName=None, operStatus=None, errorMsg=None)
line_oper_status_changed = LinesAndTract(code=u'1.1.2.6.5', operStatus=None, errorMsg=None, netName=None)
tr_oper_status_changed = LinesAndTract(code=u'1.1.2.6.6', operStatus=None, errorMsg=None, netName=None)
person_changed = UsersAndRoles(code=u'1.2.5', personName=None, message=None)
person_status_changed = UsersAndRoles(code=u'1.2.6', personName=None, personStatus=None)
work_complite = JournalOfActions(code=u'1.3.2.4', workGUI=None, personName=None)
work_comment = JournalOfActions(code=u'1.3.2.6', workGUI=None, personName=None)
document_content_added = Documents(code=u'1.3.3.3', contentName=None)
document_action_overdue = Documents(code=u'1.3.3.7', actionType=None)
task_error = MetaData(code=u'1.4.6', taskName=None, errorMsg=None)
incedent_added = MetaData(code=u'1.4.7', taskName=None, message=None)

listOfClasses = [addseg_oper_status_changed, cc_service, tko_changed, tko_oper_status_changed, ds_oper_status_changed,
                 obj_adm_status_changed,
                 soft_adm_status_changed, soft_oper_status_changed, line_oper_status_changed, tr_oper_status_changed,
                 person_changed, person_status_changed, work_complite, work_comment, document_content_added,
                 document_action_overdue,
                 task_error, incedent_added]
codes = (
    u'1.1.1.10', u'1.1.1.5.9', u'1.1.1.5.5', u'1.1.1.6.12', u'1.1.1.6.11', u'1.1.1.7.1.8', u'1.1.1.7.1.7', u'1.1.2.6.5',
    u'1.1.2.6.6', u'1.2.5', u'1.2.6', u'1.3.2.4', u'1.3.2.6', u'1.3.3.3', u'1.3.3.7', u'1.4.6', u'1.4.7')

if __name__ == '__main__':
    pass
