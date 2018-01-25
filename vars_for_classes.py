# -*- coding: UTF-8 -*-

import datetime
import pprint
from random import randint as random
from classes_for_db import ZCandUS, OM, UsersAndRoles

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
                  estADDSEG: u'дополнитльный сегмент'}
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
id = (
    '1.1.1.4', '1.1.1.6.1', '1.1.1.6.2', '1.1.1.6.3', '1.1.1.6.7', '1.1.1.6.8', '1.1.1.6.9', '1.1.1.6.10', '1.1.1.6.12',
    '1.1.1.6.13', '1.1.1.7.1.1', '1.1.1.7.1.2', '1.1.1.7.1.4', '1.1.1.7.1.5', '1.1.1.7.1.8', '1.1.1.7.1.7',
    '1.1.1.7.1.9',
    '1.1.2.6.6', '1.4.1', '1.4.2', '1.4.3', '1.4.4', '1.4.5', '1.4.6', '1.4.7', '1.1.1.10', '1.1.1.1', '1.1.1.2',
    '1.1.1.8',
    '1.1.1.9', '1.1.1.5.1', '1.1.1.5.2', '1.1.1.5.3', '1.1.1.5.5', '1.1.2.1', '1.1.2.2', '1.1.2.5', '1.1.2.6.1',
    '1.1.2.6.2',
    '1.2.1', '1.2.2', '1.2.3', '1.2.4', '1.2.5', '1.2.6', '1.3.1.1', '1.3.2.1', '1.3.2.2', '1.3.2.3', '1.3.2.4',
    '1.3.2.5', '1.3.2.6',
    '1.3.3.0', '1.3.3.1', '1.3.3.2', '1.3.3.3', '1.3.3.4', '1.3.3.5', '1.3.3.6', '1.3.3.7', '1.3.3.8', '1.3.3.9',
    '1.3.3.10', '1.3.3.11')
dictIdDesc = {id[0]: u'Добавлен УС', id[1]: u'Удален УС', id[2]: u'Добавлен ОМ', id[3]: u'Удален ОМ',
              id[4]: u'Изменение ОС ОМ',
              id[5]: u'Изменены параметры ОМ',
              id[6]: u'Изменены параметры доступа ОМ', id[7]: u'Добавлен ИД', id[8]: u'Удален ИД',
              id[9]: u'Изменение административного состояния ОМ',
              id[10]: u'Изменение ОС ИД', id[11]: u'Изменены параметры доступа ИД', id[12]: u'Добавлено ПС',
              id[13]: u'Удалено ПС', id[14]: u'Запущено ПС',
              id[15]: u'Остановлено ПС', id[16]: u'Изменение административного состояния ПС',
              id[17]: u'Изменение ОС ПС',
              id[18]: u'Изменена конфигурация ПС', id[19]: u'Изменение ОС линии связи',
              id[20]: u'Изменение ОС тракта', id[21]: u'Добавлен класс метаданных',
              id[22]: u'Удален класс метаданных', id[23]: u'Добавлено задание', id[24]: u'Удалено задание',
              id[25]: u'Выполнено задание',
              id[26]: u'Ошибка выполение задания', id[27]: u'Обнаружен инцидент',
              id[28]: u'Изменение ОС дополнительного сегмента',
              id[27]: u'Добавлена ЗС', id[28]: u'Удалена ЗС', id[29]: u'Изменена структура УС',
              id[30]: u'Изменен перечень служб',
              id[31]: u'Добавлено ТКО', id[32]: u'Удалено ТКО', id[33]: u'Изменена конфигуация ТКО',
              id[34]: u'Изменение ОС ТКО',
              id[35]: u'Добавлена СС', id[36]: u'Удалена СС', id[37]: u'Изменена конфигурация СС',
              id[38]: u'Добавлена ЛС (Участок ЛС)',
              id[39]: u'Добавлена должность', id[40]: u'Удалена должность', id[41]: u'Добавлено ДЛ',
              id[42]: u'Удалено ДЛ',
              id[43]: u'Изменены полномочия ДЛ', id[44]: u'Изменен статус ДЛ', id[45]: u'Очищен журнал событий',
              id[46]: u'Очищен журнал действий',
              id[47]: u'Создано действие', id[48]: u'Просрочено действие', id[49]: u'Действие выполнено',
              id[50]: u'Отказ выполнить действие',
              id[51]: u'Изменен комментарий действия', id[52]: u'Сформирован черновик',
              id[53]: u'Сформирован документ', id[54]: u'Документ отредактирован',
              id[55]: u'Добавлено вложение', id[56]: u'Удалено вложение', id[57]: u'Документ помещен в архив',
              id[58]: u'Выполнено действие над документом',
              id[59]: u'Просрочено действие над документом', id[60]: u'Добавлена задача', id[61]: u'Удалена задача',
              id[62]: u'Документ отправлен по почте',
              id[63]: u'Вложение выгружено на диск'}

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
asNOT_USED = 0
asUSED = 1

admStatusNames = {
    asNOT_USED: u"не используется",
    asUSED: u"используется"
}

psDUTY = 0
psPLACE = 1
psTRIP = 2
psFREE = 3
psSICK = 4

personStatusNames = {
    psDUTY: u"смена",
    psPLACE: u"служба",
    psTRIP: u"командировка",
    psFREE: u"отпуск",
    psSICK: u"больничный",
}


def generationEvents():
    """Возвращает list словарей из классов"""
    startdate = datetime.date(2017, 01, 01)
    randomdate = startdate + datetime.timedelta(random(1, 365))
    time = datetime.time(random(1, 23), random(1, 59), random(1, 59))
    date = datetime.datetime.combine(randomdate, time)

    ccAdded = ZCandUS(created=date, code=id[0], severity=severityDic[esINFO],
                      category=eventCategoryDic[ecADMINISTRATION],
                      sourceType=eventSourceDic[
                          estADMINISTRATOR], sourceId=estADMINISTRATOR, zcName='точка ыва').messageFromClass(
        dictIdDesc[id[0]])
    ccDeleted = ZCandUS(created=date, code=id[1], severity=severityDic[esINFO],
                        category=eventCategoryDic[ecADMINISTRATION],
                        sourceType=eventSourceDic[estADMINISTRATOR], sourceId=estADMINISTRATOR,
                        zcName='точка ыва').messageFromClass(dictIdDesc[id[1]])
    obj_added = OM(created=date, code=id[2], severity=severityDic[esINFO], category=eventCategoryDic[ecADMINISTRATION],
                   sourceType=eventSourceDic[estADMINISTRATOR],
                   sourceId=estADMINISTRATOR, zcName='выфвф', objName='рофлцу', className='арр').messageFromClass(
        dictIdDesc[id[2]])
    obj_deleted = OM(created=date, code=id[3], severity=severityDic[esINFO],
                     category=eventCategoryDic[ecADMINISTRATION],
                     sourceType=eventSourceDic[estADMINISTRATOR],
                     sourceId=estADMINISTRATOR,
                     zcName='rosdf', objName='рофлцй', className='dfssfsd').messageFromClass(dictIdDesc[id[3]])
    obj_operstatus_changed = OM(created=date, code=id[4], severity=None, category=eventCategoryDic[ecMONITORING],
                                sourceType=eventSourceDic[estSERVER], sourceId=estSERVER,
                                objName='fds', className='asdas',
                                operStatus=osNOT_ACCESSIBLE,
                                errorMsg=operStatusNames[osNOT_ACCESSIBLE]).messageFromClass(
        dictIdDesc[id[4]])

    obj_params_changed = OM(created=date, code=id[5], severity=severityDic[esINFO],
                            category=eventCategoryDic[ecADMINISTRATION],
                            sourceType=eventSourceDic[estADMINISTRATOR], sourceId=estADMINISTRATOR, objName='saddas',
                            className='adssad').messageFromClass(dictIdDesc[id[5]])
    obj_access_changed = OM(created=date, code=id[6], severity=severityDic[esINFO],
                            category=eventCategoryDic[ecADMINISTRATION],
                            sourceType=eventSourceDic[estADMINISTRATOR], sourceId=estADMINISTRATOR, objName='dasdsa',
                            className='dasdsadwe').messageFromClass(dictIdDesc[id[6]])
    ds_added = OM(created=date, code=id[7], severity=severityDic[esINFO], category=eventCategoryDic[ecADMINISTRATION],
                  sourceType=eventSourceDic[estADMINISTRATOR],
                  sourceId=estADMINISTRATOR, dsName='dsadsa', dsType='asdasd').messageFromClass(dictIdDesc[id[7]])
    obj_adm_status_changed = OM(created=date, code=id[8], severity=None, category=eventCategoryDic[ecADMINISTRATION],
                                sourceType=eventSourceDic[estADMINISTRATOR],
                                sourceId=estADMINISTRATOR, objName='adssad', className='sdasd',
                                admStatus=admStatusNames[asNOT_USED]).messageFromClass(dictIdDesc[id[9]])
    addseg_oper_status_changed = ZCandUS(created=date, code=id[28], severity=None,
                                         category=eventCategoryDic[ecMONITORING],
                                         sourceType=eventSourceDic[estSERVER], sourceId=estSERVER,
                                         operStatus=operStatusNames[osALERT]).messageFromClass(dictIdDesc[id[28]])
    person_status_changed = UsersAndRoles(created=date, code=id[44], severity=severityDic[esINFO],
                                          category=eventCategoryDic[ecADMINISTRATION],
                                          sourceType=eventSourceDic[estADMINISTRATOR], sourceId=estADMINISTRATOR,
                                          postName='ralal',
                                          personName='sadas', personStatus=personStatusNames[psFREE]).messageFromClass(
        dictIdDesc[id[44]])
    # лист из ужаса наверху
    classes = [ccAdded, ccDeleted, obj_added, obj_deleted, obj_params_changed, obj_operstatus_changed,
               obj_access_changed, obj_adm_status_changed,
               ds_added, addseg_oper_status_changed, person_status_changed]
    return classes


def randomEvent(number):
    """возвращает рандомный словарь из класса"""
    for i in range(0, number):
        list = generationEvents()
        var = list.pop(random(0, len(list) - 1))
        return var


if __name__ == '__main__':
    pass
