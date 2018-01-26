# -*- coding: UTF-8 -*-
import time
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
    """вставка событий в бд"""
    for i in xrange(numbers):
        db.Events.insert(generationEvents())
        if i % 1000 == 0:
            print 'прошло 1000 записей'
    print 'program finished'
    client.close()


if __name__ == '__main__':
    numbers = int(raw_input('> '))
    try:
        insertingIntoBD(numbers)
    finally:
        client.close()
