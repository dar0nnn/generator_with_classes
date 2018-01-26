# -*- coding: UTF-8 -*-
import time
from pymongo import MongoClient
from vars_for_classes import generationEvents


def timeit(method):  # замер времени
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result

    return timed


try:  # подключение к бд
    client = MongoClient('192.168.62.129', 27017)
    db = client.Events
    events = db.Events
    events.delete_many({})
except Exception as e:
    print e
    client.close()

@timeit
def insertingIntoBD(numbers):
    for i in xrange(numbers):
        db.Events.insert(generationEvents())
        if i % 1000 == 0:
            print 'прошло 1000 записей'
    # for event in events.find({}).limit(5):
    #     for k, v in event.items():
    #         print k, v
    print 'program finished'
    client.close()


if __name__ == '__main__':
    numbers = int(raw_input('> '))
    try:
        insertingIntoBD(numbers)
    finally:
        client.close()
