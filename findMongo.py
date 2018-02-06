# -*- coding: UTF-8 -*-
import locale
import time
import re
import datetime

import sys
from pymongo import MongoClient

reload(sys)
sys.setdefaultencoding('utf-8')
locale.setlocale(locale.LC_ALL, '')

# для тестов mongo
# определять время поиска по бд

try:
    client = MongoClient('192.168.62.129', 27017)
    db = client.Events
    events = db.Events
except Exception as e:
    print e

nov = datetime.datetime(2017, 11, 12, 00, 00, 00)
dec = datetime.datetime(2017, 12, 31, 22, 00, 00)
jan = datetime.datetime(2017, 01, 12)
feb = datetime.datetime(2017, 02, 10)
oct = datetime.datetime(2017, 10, 1)


def timeit(method):
    def timed(*args, **kw):
        """замер времени"""
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print(u'%r  %2.2f ms' % (method.__name__, (te - ts) * 10000))
        return result

    return timed


@timeit
def findFirst():
    """3249 события 25284 ms"""
    nov_event = events.find({u'severity': u'1', u'sourceType': u'1', u'code': u'1.1.1.10', u'created': {u'$gt': nov},
                             u"params.operStatus": u"1"})

    print u'nov events ', nov_event.count()


@timeit
def findSecond():
    """282 события 25114 ms"""
    dec_event = events.find({u'severity': u'2', u'sourceType': u'0', u'code': u'1.1.1.6.11', u'created': {u'$gt': dec}})
    print u'dec events ', dec_event.count()


@timeit
def findThird():
    """2395 событий 24094 ms"""
    janAndFebEvent = events.find({u'created': {"$gt": jan, "$lt": feb}, u'code': u'1.2.5', u'sourceType': u'0',
                                  u'sourceId': u"сервер", u'severity': u'0'})
    print u'jan and feb ', janAndFebEvent.count()


@timeit
def findForth():
    """70604 событий 24971 ms"""
    oct_search = events.find({u'created': {"$gt": oct}, u'code': u'1.1.1.7.1.8', u'sourceType': u'1'})
    print u'oct search ', oct_search.count()


@timeit
def totalTime():
    """total time: 99466 ms"""
    findFirst()
    findSecond()
    findThird()
    findForth()
    print u'end of total time func'
    client.close()


if __name__ == '__main__':
    totalTime()
