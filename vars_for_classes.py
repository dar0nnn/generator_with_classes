# -*- coding: UTF-8 -*-

import datetime
import random

from classes_for_db import ZCandUS, TKO, OM, PS, LinesAndTract, UsersAndRoles, JournalOfActions, \
    Documents, MetaData

# severity
esINFO = 0
esWARNING = 1
esALERT = 2
esCRITICAL = 3

severityDic = {esINFO: u'информация',
               esWARNING: u'предупреждение',
               esALERT: u'авария',
               esCRITICAL: u'критично'}

# eventSource
estSERVER = 0
estADMINISTRATOR = 1
estADDSEG = 5

eventSourceDic = {estSERVER: u'сервер',
                  estADMINISTRATOR: u'администратор',
                  estADDSEG: u'дополнительный сегмент'}
# eventCategory
ecADMINISTRATION = 1
ecMONITORING = 2
ecMANAGEMENT = 3
ecSECURITY = 4
ecFUNCTION = 5

eventCategoryDic = {ecADMINISTRATION: u'администрирование',
                    ecMONITORING: u'мониторинг',
                    ecMANAGEMENT: u'управление',
                    ecSECURITY: u'безопасность',
                    ecFUNCTION: u'функционирование'}

# codes
# codeForBd = (
#     u'1.1.1.4', u'1.1.1.6.1', u'1.1.1.6.2', u'1.1.1.6.3', u'1.1.1.6.7', u'1.1.1.6.8', u'1.1.1.6.9', u'1.1.1.6.10',
#     u'1.1.1.6.12',
#     u'1.1.1.6.13', u'1.1.1.7.1.1', u'1.1.1.7.1.2', u'1.1.1.7.1.4', u'1.1.1.7.1.5', u'1.1.1.7.1.8', u'1.1.1.7.1.7',
#     u'1.1.1.7.1.9',
#     u'1.1.2.6.6', u'1.4.1', u'1.4.2', u'1.4.3', u'1.4.4', u'1.4.5', u'1.4.6', u'1.4.7', u'1.1.1.10', u'1.1.1.1',
#     u'1.1.1.2',
#     u'1.1.1.8',
#     u'1.1.1.9', u'1.1.1.5.1', u'1.1.1.5.2', u'1.1.1.5.3', u'1.1.1.5.5', u'1.1.2.1', u'1.1.2.2', u'1.1.2.5',
#     u'1.1.2.6.1',
#     u'1.1.2.6.2',
#     u'1.2.1', u'1.2.2', u'1.2.3', u'1.2.4', u'1.2.5', u'1.2.6', u'1.3.1.1', u'1.3.2.1', u'1.3.2.2', u'1.3.2.3',
#     u'1.3.2.4',
#     u'1.3.2.5', u'1.3.2.6',
#     u'1.3.3.0', u'1.3.3.1', u'1.3.3.2', u'1.3.3.3', u'1.3.3.4', u'1.3.3.5', u'1.3.3.6', u'1.3.3.7', u'1.3.3.8',
#     u'1.3.3.9',
#     u'1.3.3.10', u'1.3.3.11')
# dictIdDesc = {codeForBd[0]: u'Добавлен УС', codeForBd[1]: u'Удален УС', codeForBd[2]: u'Добавлен ОМ',
#               codeForBd[3]: u'Удален ОМ',
#               codeForBd[4]: u'Изменение ОС ОМ',
#               codeForBd[5]: u'Изменены параметры ОМ',
#               codeForBd[6]: u'Изменены параметры доступа ОМ', codeForBd[7]: u'Добавлен ИД', codeForBd[8]: u'Удален ИД',
#               codeForBd[9]: u'Изменение административного состояния ОМ',
#               codeForBd[10]: u'Изменение ОС ИД', codeForBd[11]: u'Изменены параметры доступа ИД',
#               codeForBd[12]: u'Добавлено ПС',
#               codeForBd[13]: u'Удалено ПС', codeForBd[14]: u'Запущено ПС',
#               codeForBd[15]: u'Остановлено ПС', codeForBd[16]: u'Изменение административного состояния ПС',
#               codeForBd[17]: u'Изменение ОС ПС',
#               codeForBd[18]: u'Изменена конфигурация ПС', codeForBd[19]: u'Изменение ОС линии связи',
#               codeForBd[20]: u'Изменение ОС тракта', codeForBd[21]: u'Добавлен класс метаданных',
#               codeForBd[22]: u'Удален класс метаданных', codeForBd[23]: u'Добавлено задание',
#               codeForBd[24]: u'Удалено задание',
#               codeForBd[25]: u'Выполнено задание',
#               codeForBd[26]: u'Ошибка выполение задания', codeForBd[27]: u'Обнаружен инцидент',
#               codeForBd[28]: u'Изменение ОС дополнительного сегмента',
#               codeForBd[27]: u'Добавлена ЗС', codeForBd[28]: u'Удалена ЗС', codeForBd[29]: u'Изменена структура УС',
#               codeForBd[30]: u'Изменен перечень служб',
#               codeForBd[31]: u'Добавлено ТКО', codeForBd[32]: u'Удалено ТКО',
#               codeForBd[33]: u'Изменена конфигуация ТКО',
#               codeForBd[34]: u'Изменение ОС ТКО',
#               codeForBd[35]: u'Добавлена СС', codeForBd[36]: u'Удалена СС', codeForBd[37]: u'Изменена конфигурация СС',
#               codeForBd[38]: u'Добавлена ЛС (Участок ЛС)',
#               codeForBd[39]: u'Добавлена должность', codeForBd[40]: u'Удалена должность',
#               codeForBd[41]: u'Добавлено ДЛ',
#               codeForBd[42]: u'Удалено ДЛ',
#               codeForBd[43]: u'Изменены полномочия ДЛ', codeForBd[44]: u'Изменен статус ДЛ',
#               codeForBd[45]: u'Очищен журнал событий',
#               codeForBd[46]: u'Очищен журнал действий',
#               codeForBd[47]: u'Создано действие', codeForBd[48]: u'Просрочено действие',
#               codeForBd[49]: u'Действие выполнено',
#               codeForBd[50]: u'Отказ выполнить действие',
#               codeForBd[51]: u'Изменен комментарий действия', codeForBd[52]: u'Сформирован черновик',
#               codeForBd[53]: u'Сформирован документ', codeForBd[54]: u'Документ отредактирован',
#               codeForBd[55]: u'Добавлено вложение', codeForBd[56]: u'Удалено вложение',
#               codeForBd[57]: u'Документ помещен в архив',
#               codeForBd[58]: u'Выполнено действие над документом',
#               codeForBd[59]: u'Просрочено действие над документом', codeForBd[60]: u'Добавлена задача',
#               codeForBd[61]: u'Удалена задача',
#               codeForBd[62]: u'Документ отправлен по почте',
#               codeForBd[63]: u'Вложение выгружено на диск'}

codeForBd = (
    u'1.1.1.10', u'1.1.1.9', u'1.1.1.5.5', u'1.1.1.6.12', u'1.1.1.6.11', u'1.1.1.7.1.8', u'1.1.1.7.1.7', u'1.1.2.6.5',
    u'1.1.2.6.6', u'1.2.5', u'1.2.6', u'1.3.2.4', u'1.3.2.6', u'1.3.3.3', u'1.3.3.7', u'1.4.6', u'1.4.7')

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
              codeForBd[16]: u'Обнаружен инцидент'}


# oper status
osUNDEFINED = 0
osNORM = 1
osNOT_ACCESSIBLE = 2
osALERT = 3

operStatusNames = {
    osUNDEFINED: u"не определено",
    osNORM: u"норма",
    osNOT_ACCESSIBLE: u"не доступен",
    osALERT: u"авария"
}
# adm status
asNOT_USED = 0
asUSED = 1

admStatusNames = {
    asNOT_USED: u"не используется",
    asUSED: u"используется"
}
# person status
psDUTY = 0
psPLACE = 1
psTRIP = 2
psFREE = 3
psSICK = 4

personStatusValues = (psDUTY, psPLACE, psTRIP, psFREE, psSICK)

personStatusNames = {
    psDUTY: u"смена",
    psPLACE: u"служба",
    psTRIP: u"командировка",
    psFREE: u"отпуск",
    psSICK: u"больничный",
}

# segment
seRED = 0
seBLUE = 1
segmentValues = (seRED, seBLUE)

opADD = 0
opDEL = 1

operationValues = (opADD, opDEL)

# docType
docTYPE1 = 0
docTYPE2 = 1
docTYPE3 = 2
docTYPE4 = 3
docTYPE5 = 4
docTYPE6 = 5
docTYPE7 = 6
docTYPE8 = 7
docTYPE9 = 8

docTypeValues = (docTYPE1, docTYPE2, docTYPE3, docTYPE4, docTYPE5, docTYPE6, docTYPE7, docTYPE8, docTYPE9)

#  actionType
atCREATE = 0
atACQUIRE = 1
atINTRO = 2
atALIGN = 3
atEDIT = 4
atARCHIVE = 5
atSEND = 6
atACTIVE = 7
atCONTADD = 8
atCONTDEL = 9
atACTIONADD = 10
atACTIONDEL = 11
atEXECUTE = 12
atSTATE = 13

actionTypeValues = (
    atCREATE, atACQUIRE, atINTRO, atALIGN, atEDIT, atARCHIVE, atSEND, atACTIVE, atCONTADD, atCONTDEL, atACTIONADD,
    atACTIONDEL, atEXECUTE, atSTATE)

# 8. lType
ltPHISICAL = 0
ltETHERNET = 1
ltSDH = 2
ltPDF = 3

lTypeValues = (ltPHISICAL, ltETHERNET, ltSDH, ltPDF)


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

# {'created': createdGen(), 'code': codeGen().next(), 'severity': severityGen(),
#  'category': category_gen(),
#  'sourceType': sourceTypeGen(),
#  'sourceId': sourceIdGen().next(), 'zcName': stringGen, 'ccName': stringGen, 'services': operationGen,
#  'operStatusMessage': stringGen, 'errorMsg': stringGen, 'objName': stringGen, 'className': stringGen,
#  'dsName': stringGen, 'dsType': stringGen, 'operStatus': oper_status_gen, 'admStatus': stringGen,'softName': stringGen}

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
    codeForMessage = None  # для описания кода
    item = random.choice(listOfClasses)  # выбор класса из списка
    eventDesc = {'created': createdGen(), 'code': codeGen().next(), 'severity': severityGen(),
                 'category': category_gen(),
                 'sourceType': sourceTypeGen(),
                 'sourceId': sourceIdGen().next(), 'zcName': stringGen(), 'ccName': stringGen(), 'services': operationGen(),
                 'operStatusMessage': stringGen(), 'errorMsg': stringGen(), 'objName': stringGen(), 'className': stringGen(),
                 'dsName': stringGen(), 'dsType': stringGen(), 'operStatus': oper_status_gen(), 'admStatus': stringGen(),
                 'softName': stringGen()}  # генерируется словарь значений для полей класса
    varOfClass = [x for x in dir(item) if
                  not x.startswith('_') and x != 'messageFromClass']  # получение переменных класса для заполнения
    for key in eventDesc.keys():  # пробежка по ключам словаря
        if key in varOfClass: # сравнение ключа с переменной, содержащейся в классе
            varName = key  # отвечает за название поля класса
            if varName is 'code':  # для нахождения кода
                codeForMessage = eventDesc[
                    varName]  # и записи его в переменную для описания кода в .messageFromClass
            varValue = eventDesc[key]  # значение поля класса
            item.__setattr__(varName, varValue)  # присвоение значения
        else:
            continue
    return item.messageFromClass(codeForMessage)  # возврат словаря поле класса - значение и описания события


if __name__ == '__main__':
    x = generationEvents()
    print type(x)
    for k, v in x.items():
        print k, '-----------', v
