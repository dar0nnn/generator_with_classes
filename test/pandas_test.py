# -*-coding: utf-8 -*-
import time
import datetime
from pymongo import MongoClient
from vars_for_classes import generationEvents as gen
import json


def timeit(method):
    def timed(*args, **kw):
        """замер времени"""
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('%r  %2.2f s' % (method.__name__, (te - ts)))
        return result
    return timed

def myconverter(o): #to convert data in str
    if isinstance(o, datetime.datetime):
        return o.__str__()


@timeit
def writingJson(numbers):
    list_ = []
    dict_ = {}
    FILENAME = 'result.json'
    with open(FILENAME, 'w') as fp:
        for i in xrange(numbers):
            dictFromClass = gen()
            list_.append(dictFromClass)
            if i % 1000 == 0:
                print 'прошло {} генераций события и записи в лист' .format(i)
        dict_['A'] = list_
        json.dump(dict_, fp, default=myconverter)

@timeit
def writingMongo():
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
            parsed = json.loads(fp.read()) # <--- dict
            for dictForMongo in parsed.values(): # parsed.values возвращает лист словарей, проход по этому листу и вытягивание одного словаря
                db.Events.insert(dictForMongo)
    finally:
        client.close()

if __name__ == '__main__':
    numbers = int(raw_input('> '))
    writingJson(numbers)
    writingMongo()