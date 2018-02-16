# -*- coding: UTF-8 -*-
import csv
import json
import time
import datetime
from pymongo import MongoClient
from vars_for_classes import generationEvents
import sys, locale, re

reload(sys)
sys.setdefaultencoding('utf-8')
locale.setlocale(locale.LC_ALL, '')

vars = [u'created', u'code', u'category', u'sourceType', u'sourceId', u'severity', u'description']
FIELDNAMESFORCSV = (
    u'category', u'code', u'sourceType', u'created', u'sourceId', u'description', u'severity', u'segment',
    u'services', u'operation', u'zcName', u'ccName', u'operStatus', u'errorMsg', u'segment', u'unitName', u'unitType',
    u'dsName', u'dsType', u'objName', u'className', u'admStatus', u'softName', u'familyName', u'lName', u'lType',
    u'netName', u'personName', u'message', u'postName', u'personStatus', u'workGUI', u'docName', u'docType',
    u'contentName', u'actionType', u'message', u'metaName', u'taskName')
FILECSV = 'result.csv'
FILENAME0 = 'result0.json'
FILENAME1 = 'result1.json'
FILENAME2 = 'result2.json'
FILENAME3 = 'result3.json'
FILENAME4 = 'result4.json'
FILENAME5 = 'result5.json'
FILENAME6 = 'result6.json'
FILENAME7 = 'result7.json'
FILENAME8 = 'result8.json'
FILENAME9 = 'result9.json'
listOfFiles = (
    FILENAME0, FILENAME1, FILENAME2, FILENAME3, FILENAME4, FILENAME5, FILENAME6, FILENAME7, FILENAME8, FILENAME9)


def timeit(method):
    def timed(*args, **kw):
        """замер времени"""
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print(u'%r  %2.2f m' % (method.__name__, (te - ts) / 60))
        return result

    return timed


@timeit
def writingDirectlyToMongo(numbers):
    """вставка событий напрямую в бд"""
    try:
        try:  # подключение к бд
            client = MongoClient('192.168.62.129', 27017)
            db = client.Events
            events = db.Events
            events.delete_many({})
        except Exception as e:
            print e
        for i in xrange(numbers):
            db.Events.insert(generationEvents())
            if i % 1000 == 0:
                print u'прошло {} записей'.format(i)
        print u'program finished'
    finally:
        client.close()


def dateToSting(dateFromClass):  # функция для json.dump что бы преобразовать дату в стринг
    if isinstance(dateFromClass, datetime.datetime):
        return dateFromClass.__str__()


@timeit
def writingToCsv(numbers):
    """запись данных в csv"""
    with open(FILECSV, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMESFORCSV)
        writer.writeheader()
        for i in xrange(numbers):
            dictForCsv = generationEvents()
            for k, v in dictForCsv.items():
                if k == u'params':
                    for key_, value_ in dictForCsv[u'params'].items():
                        dictForCsv[key_] = value_
            dictForCsv.pop(u'params', None)
            writer.writerow(dictForCsv)


@timeit
def writingJson(numbers):
    """запись данных в 10 json файлов"""
    dictForJson = {}
    for file_ in listOfFiles:
        with open(file_, 'w') as fp:
            listOfDicts = []
            for i in xrange(numbers / 10):
                dictFromClass = generationEvents()
                listOfDicts.append(dictFromClass)
                if i % 1000 == 0:
                    print u'прошло {} генераций события и записи в {}'.format(i, file_)
            dictForJson['A'] = listOfDicts
            json.dump(dictForJson, fp, default=dateToSting)


@timeit
def writingMongoFromJson():
    """чтение 10 json файлов и запись их в бд"""
    try:
        try:
            client = MongoClient('192.168.62.129', 27017)
            db = client.Events
            events = db.Events
            events.delete_many({})  # стирает записи из бд!!!
        except Exception as e:
            print e
        for file__ in listOfFiles:
            with open(file__, 'r') as fp:
                print u'открыт {}'.format(file__)
                parsed = json.loads(fp.read())  # <--- dict
                for dictForMongo in parsed.values():  # parsed.values возвращает лист словарей,
                    # проход по этому листу и вытягивание одного словаря
                    for item in dictForMongo:
                        date = float(item['created'])
                        item['created'] = datetime.datetime.fromtimestamp(date)  # date to ISODate
                        db.Events.insert(item)
    except Exception as e:
        print e
    finally:
        client.close()


@timeit
def writingToMongoFromCsv():
    """запись в базу из csv"""
    try:
        client = MongoClient('192.168.62.129', 27017)
        db = client.Events
        events = db.Events
        events.delete_many({})  # стирает записи из бд!!!
    except Exception as e:
        print e
    with open('result.csv', 'rb') as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            dictOfParams = {}
            for k, v in row.items():
                if k not in vars:
                    if v != '':
                        dictOfParams[k] = v
                        row.pop(k, None)
                    else:
                        row.pop(k, None)
                elif k == u'created':
                    date = float(row[u'created'])
                    row[u'created'] = datetime.datetime.fromtimestamp(date)
            row[u'params'] = dictOfParams
            db.Events.insert(row)


@timeit
def writingJsonAndCsv(numbers):
    """пишет одновременно в json и в csv одинаковые значения"""
    with open(FILECSV, 'w') as f:  # open csv
        writer = csv.DictWriter(f, fieldnames=FIELDNAMESFORCSV)  # writer for dicts in csv
        writer.writeheader()  # writing keys in csv
        for file_ in listOfFiles:  # for file in list of json files
            with open(file_, 'w') as fp:  # open json
                dictForJson = {}
                listOfDicts = []
                for i in xrange(numbers / 10):
                    dictForCsv = {}  # new dict for csv
                    dictFromClass = generationEvents()  # dict for json from func
                    listOfDicts.append(dictFromClass)
                    for k, v in dictFromClass.items():  # copy one dict to another
                        dictForCsv[k] = v
                    if i % 1000 == 0:
                        print u'прошло {} генераций события и записи в {}'.format(i, file_)
                    for k, v in dictForCsv.items():
                        if k == u'params':
                            for key_, value_ in dictForCsv[u'params'].items():
                                dictForCsv[key_] = value_
                    dictForCsv.pop(u'params', None)
                    writer.writerow(dictForCsv)
                dictForJson['A'] = listOfDicts
                json.dump(dictForJson, fp, default=dateToSting)


@timeit
def writingJsonAndMongo(numbers):
    writingJson(numbers)
    writingMongoFromJson()


if __name__ == '__main__':
    numbers = int(raw_input('> '))
    writingToCsv(numbers)
