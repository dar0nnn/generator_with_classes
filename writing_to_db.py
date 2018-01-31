# -*- coding: UTF-8 -*-
import json
import time

import datetime
from pymongo import MongoClient
from vars_for_classes import generationEvents

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
    try:  # подключение к бд
        client = MongoClient('192.168.62.129', 27017)
        db = client.Events
        events = db.Events
        events.delete_many({})
    except Exception as e:
        print e
        client.close()
    try:
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
            client.close()
        for file__ in listOfFiles:
            with open(file__, 'r') as fp:
                print 'открыт {}'.format(file__)
                parsed = json.loads(fp.read())  # <--- dict
                for dictForMongo in parsed.values():  # parsed.values возвращает лист словарей,
                    # проход по этому листу и вытягивание одного словаря
                    db.Events.insert(dictForMongo)
    except Exception as e:
        print e
    finally:
        client.close()


@timeit
def writingJsonAndMongo(numbers):
    writingJson(numbers)
    writingMongoFromJson()


if __name__ == '__main__':
    numbers = int(raw_input('> '))
    writingJsonAndMongo(numbers)
