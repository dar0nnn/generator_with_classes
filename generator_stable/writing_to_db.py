# -*- coding: UTF-8 -*-
import pprint
from random import randint as random
import datetime
from pymongo import MongoClient
import event_classes

startdate = datetime.date(2017, 01, 01)

# severity
esINFO = 0
esWARNING = 1
esALERT = 2
esCRITICAL = 3

severityDic = {esINFO: 'информация',
               esWARNING: 'предупреждение',
               esALERT: 'авария',
               esCRITICAL: 'критично'}

# eventSource

estSERVER = 0
estADMINISTRATOR = 1
estADDSEG = 5

eventSourceDic = {estSERVER: 'сервер',
                  estADMINISTRATOR: 'администратор',
                  estADDSEG: 'дополнитльный сегмент'}
# eventCategory
ecADMINISTRATION = 1
ecMONITORING = 2
ecMANAGEMENT = 3
ecSECURITY = 4
ecFUNCTION = 5

eventCategoryDic = {ecADMINISTRATION: 'администрирование',
                    ecMONITORING: 'мониторинг',
                    ecMANAGEMENT: 'управление',
                    ecSECURITY: 'безопасность',
                    ecFUNCTION: 'функционирование'}

# подключение к бд

try:
    client = MongoClient('192.168.62.129', 27017)
    db = client.Events
    events = db.Events
    events.delete_many({})
except Exception as e:
    print e
    client.close()


# генерация случайных данных для инстанса
def gen(numbers, severityDic, eventSourceDic, eventCategoryDic):
    n = 0
    while n < numbers:
        randomdate = startdate + datetime.timedelta(random(1, 365))
        date = datetime.datetime.combine(randomdate, datetime.time.min)
        zc = event_classes.ZCandUS(date, esINFO, severityDic[esINFO], eventCategoryDic[ecADMINISTRATION],
                                   eventSourceDic[estADMINISTRATOR],
                                   estADMINISTRATOR, 'zcNameHere')
        tko_adm = event_classes.TKO(date, esINFO, severityDic[esINFO], eventCategoryDic[ecADMINISTRATION],
                                    eventSourceDic[estADMINISTRATOR], estADMINISTRATOR, 'zcNameHere', 'segmentHere',
                                 'unitNameHere',
                                 'unitTypeHere')
        tko_change = event_classes.TKO(date, esINFO, severityDic[esINFO], eventCategoryDic[ecMANAGEMENT],
                                       eventSourceDic[estADMINISTRATOR], estADMINISTRATOR, 'zcNameHere', 'segmentHere',
                                    'unitNameHere',
                                    'unitTypeHere', message='изменена конфигурация ТКО')
        rand = random(1, 3)
        if rand == 1:
            events.insert(zc.message())
        elif rand == 2:
            events.insert_one(tko_adm.message())
        elif rand == 3:
            events.insert_one(tko_change.message())
        n += 1


# main loop
def main(numbers):
    gen(numbers, severityDic, eventSourceDic, eventCategoryDic)
    for event in events.find({}).limit(5):
        pprint.pprint(event)
    print 'program finished'
    client.close()


if __name__ == '__main__':
    numbers = int(raw_input('> '))
    main(numbers)
