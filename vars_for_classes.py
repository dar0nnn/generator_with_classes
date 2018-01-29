# -*- coding: UTF-8 -*-

import datetime
import random
from classes_for_db import ZCandUS, TKO, OM, PS, LinesAndTract, UsersAndRoles, JournalOfActions, \
    Documents, MetaData

# eventSource
estSERVER = 0
estADMINISTRATOR = 1
estADDSEG = 5

eventSourceDic = {estSERVER: u'сервер',
                  estADMINISTRATOR: u'администратор',
                  estADDSEG: u'дополнительный сегмент'}

codeForBd = (
    u'1.1.1.10', u'1.1.1.9', u'1.1.1.5.5', u'1.1.1.6.12', u'1.1.1.6.11', u'1.1.1.7.1.8', u'1.1.1.7.1.7', u'1.1.2.6.5',
    u'1.1.2.6.6', u'1.2.5', u'1.2.6', u'1.3.2.4', u'1.3.2.6', u'1.3.3.3', u'1.3.3.7', u'1.4.6', u'1.4.7', u'1.1.1.5.3')

paramsForCodes = {codeForBd[0]: (u'operStatus', u'zcName', u'ccName'),
                  codeForBd[1]: (u'segment', u'services', u'operation', u'zcName'),
                  codeForBd[2]: (
                  u'operStatus', u'errorMsg', u'segment', u'unitName', u'unitType', u'zcName', u'ccName'),
                  codeForBd[3]: (u'dsName', u'dsType', u'operStatus', u'errorMsg', u'zcName', u'ccName'),
                  codeForBd[4]: (u'objName', u'className', u'admStatus', u'zcName', u'ccName'),
                  codeForBd[5]: (u'admStatus', u'softName', u'familyName', u'zcName', u'ccName'),
                  codeForBd[6]: (u'operStatus', u'errorMsg', u'softName', u'familyName', u'zcName', u'ccName'),
                  codeForBd[7]: (u'ccName', u'segment', u'operStatus', u'errorMsg', u'lName', u'lType', u'netName'),
                  codeForBd[8]: (u'ccName', u'segment', u'operStatus', u'errorMsg',  u'lName', u'lType', u'netName'),
                  codeForBd[9]: (u'personName', u'message', u'postName'),
                  codeForBd[10]: (u'personName', u'personStatus', u'postName'),
                  codeForBd[11]: (u'workGUI', u'personName'),
                  codeForBd[12]: (u'workGUI', u'personName'),
                  codeForBd[13]: (u'docName', u'docType', u'contentName'),
                  codeForBd[14]: (u'docName', u'docType', u'actionType'),
                  codeForBd[15]: (u'metaName', u'taskName', u'errorMsg'),
                  codeForBd[16]: (u'metaName', u'taskName', u'message'),
                  codeForBd[17]: (u'message', u'segment', u'unitName', u'unitType', u'zcName', u'ccName')}

dictIdDesc = {codeForBd[0]: u'Изменение ОС дополнительного сегмента', codeForBd[1]: u'Изменен перечень служб',
              codeForBd[2]: u'Изменение ОС ТКО', codeForBd[3]: u'Изменение ОС ИД',
              codeForBd[4]: u'Изменение административного состояния ОМ',
              codeForBd[5]: u'Изменение административного состояния ПС', codeForBd[6]: u'Изменение ОС ПС',
              codeForBd[7]: u'Изменение ОС линии связи',
              codeForBd[8]: u'Изменение ОС тракта', codeForBd[9]: u'Изменены полномочия ДЛ',
              codeForBd[10]: u'Изменен статус ДЛ',
              codeForBd[11]: u"Действие выполнено", codeForBd[12]: u"Изменен комментарий действия",
              codeForBd[13]: u"Добавлено вложение",
              codeForBd[14]: u"Просрочено действие над документом", codeForBd[15]: u'Ошибка выполнения задания',
              codeForBd[16]: u'Обнаружен инцидент', codeForBd[17]: u'Изменена конфигурация ТКО'}


# created, code, severity, category, sourceType, sourceId
def createdGen():  # рандомная дата
    startdate = datetime.date(2017, 01, 01)
    randomdate = startdate + datetime.timedelta(random.randint(1, 365))
    time = datetime.time(random.randint(1, 23), random.randint(1, 59), random.randint(1, 59))
    return datetime.datetime.combine(randomdate, time)


sourceIdValues = eventSourceDic.values()  # список id источников события
stringGen = lambda: ''.join(
    random.choice(u'йцукенгшщзхъфывапролджэячсмитьбю') for i in range(random.randint(5, 10)))  # рандомный текст
category_gen = lambda: random.choice(range(1, 5))  # # рандомная категория
oper_status_gen = lambda: random.choice(range(1, 5))  # рандомный статус
severityGen = lambda: random.choice(range(0, 3))  # рандомная важность
sourceTypeGen = lambda: random.choice(range(0, 2))  # рандомный тип источника
sourceIdGen = lambda: (random.choice(sourceIdValues) for i in
                       range(0, len(sourceIdValues)))  # generator!!! .next() генерация рандомного id источника
codeGen = lambda: (random.choice(codeForBd) for i in
                   range(0, len(codeForBd)))  # generator!!! .next() рандомная генерация кода
operationGen = lambda: random.choice(range(0, 1))
admStatusGen = lambda: random.choice(range(0, 1))
personStatusGen = lambda: random.choice(range(0, 4))
lTypeGen = lambda: random.choice(range(0, 3))
segmentGen = lambda: random.choice(range(0, 1))
docTypeGen = lambda: random.choice(range(0, 8))
actionTypeGen = lambda: random.choice(range(0, 13))

# шаблоны событий
addseg_oper_status_changed = ZCandUS()
cc_service = ZCandUS()
tko_changed = TKO()
tko_oper_status_changed = TKO()
ds_oper_status_changed = OM()
obj_adm_status_changed = OM()
soft_adm_status_changed = PS()
soft_oper_status_changed = PS()
line_oper_status_changed = LinesAndTract()
tr_oper_status_changed = LinesAndTract()
person_changed = UsersAndRoles()
person_status_changed = UsersAndRoles()
work_complite = JournalOfActions()
work_comment = JournalOfActions()
document_content_added = Documents()
document_action_overdue = Documents()
task_error = MetaData()
incedent_added = MetaData()

# лист классов событий сверху
listOfClasses = [addseg_oper_status_changed, cc_service, tko_changed, tko_oper_status_changed, ds_oper_status_changed,
                 obj_adm_status_changed,
                 soft_adm_status_changed, soft_oper_status_changed, line_oper_status_changed, tr_oper_status_changed,
                 person_changed, person_status_changed, work_complite, work_comment, document_content_added,
                 document_action_overdue,
                 task_error, incedent_added]


def generationEvents():
    """генерация классов для описания события и просвоение значения полям этого класса"""
    codeForMessage = codeGen().next()  # для описания кода
    item = random.choice(listOfClasses)  # выбор класса из списка
    setOfParams = {u'created', u'code', u'severity', u'category', u'sourceType', u'sourceId'}
    for i in paramsForCodes[codeForMessage]:
        setOfParams.add(i)
    eventDesc = {u'created': createdGen(), u'code': codeForMessage, u'severity': severityGen(),
                 u'category': category_gen(),
                 u'sourceType': sourceTypeGen(),
                 u'sourceId': sourceIdGen().next(), u'zcName': stringGen(), u'ccName': stringGen(),
                 u'services': operationGen(),
                 u'message': stringGen(), u'errorMsg': stringGen(), u'objName': stringGen(),
                 u'className': stringGen(),
                 u'dsName': stringGen(), u'dsType': stringGen(), u'operStatus': oper_status_gen(),
                 u'softName': stringGen(), u'familyName': stringGen(), u'admStatus': admStatusGen(),
                 u'postName': stringGen(),
                 u'personName': stringGen(), u'personStatus': personStatusGen(), u'workGUI': stringGen(),
                 u'lName': stringGen(), u'lType': lTypeGen(),
                 u'lpFrom': stringGen(), u'lpTo': stringGen(), u'segment': segmentGen(), u'docName': stringGen(),
                 u'docType': docTypeGen(),
                 u'contentName': stringGen(), u'actionType': actionTypeGen(), u'metaName': stringGen(),
                 u'taskName': stringGen()}  # генерируется словарь значений для полей класса
    varOfClass = {x for x in dir(item) if
                  not x.startswith('_') and x != 'messageFromClass'}  # получение переменных класса для заполнения
    compliteSet = setOfParams.intersection(varOfClass)
    for key in eventDesc.keys():  # пробежка по ключам словаря
        if key in compliteSet:  # сравнение ключа с переменной, содержащейся в классе
            item.__setattr__(key, eventDesc[key])  # присвоение значения
        else:
            continue
    return item.messageFromClass(
        dictIdDesc[codeForMessage])  # возврат словаря поле класса - значение и описания события


if __name__ == '__main__':
    for i in xrange(12):
        x = generationEvents()
    print type(x)
    for k, v in x.items():
        print k, '-----------', v
