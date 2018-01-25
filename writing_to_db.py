# -*- coding: UTF-8 -*-
import time
from pymongo import MongoClient
from vars_for_classes import randomEvent


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
def gen(numbers):
    """вставка в бд случайных событий"""
    n = 0
    while n < numbers:
        db.Events.insert(randomEvent(numbers))
        n += 1


@timeit
def main(numbers):
    gen(numbers)
    for event in events.find({}).limit(5):
        for k, v in event.items():
            print k, v
    print 'program finished'
    client.close()


if __name__ == '__main__':
    numbers = int(raw_input('> '))
    try:
        main(numbers)
    finally:
        client.close()
