# -*- coding: UTF-8 -*-
import json
import time

import datetime
from pymongo import MongoClient
from vars_for_classes import generationEvents


def timeit(method):
    def timed(*args, **kw):
        """замер времени"""
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result

    return timed


@timeit
def writingDirectlyToMongo(numbers):
    """вставка событий в бд"""
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
                print 'прошло {} записей'.format(i)
        print 'program finished'
    finally:
        client.close()


def myconverter(o):  # to convert data in str
    if isinstance(o, datetime.datetime):
        return o.__str__()


@timeit
def writingJson(numbers):
    listOfDicts = []
    dictForJson = {}
    FILENAME = 'result.json'
    with open(FILENAME, 'w') as fp:
        for i in xrange(numbers):
            dictFromClass = generationEvents()
            listOfDicts.append(dictFromClass)
            if i % 1000 == 0:
                print 'прошло {} генераций события и записи в лист'.format(i)
        dictForJson['A'] = listOfDicts
        json.dump(dictForJson, fp, default=myconverter)


@timeit
def writingMongoFromJson():
    try:
        try:
            client = MongoClient('192.168.62.129', 27017)
            db = client.Events
            events = db.Events
            events.delete_many({})
        except Exception as e:
            print e
            client.close()
        FILENAME = 'result.json'
        with open(FILENAME, 'r') as fp:
            parsed = json.loads(fp.read())  # <--- dict
            for dictForMongo in parsed.values():  # parsed.values возвращает лист словарей,
                # проход по этому листу и вытягивание одного словаря
                db.Events.insert(dictForMongo)
    finally:
        client.close()


@timeit
def writingJsonAndMongo(numbers):
    writingJson(numbers)
    writingMongoFromJson()


if __name__ == '__main__':
    numbers = int(raw_input('> '))
    writingJsonAndMongo(numbers)
