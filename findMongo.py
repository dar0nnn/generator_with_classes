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
def simpleSmallCount():
    smallVarFromMongo = events.find({u'severity': u'1', u'params.admStatus': u'0', u'code': u'1.1.1.6.11',
                                     u'created': {u'$gt': datetime.datetime(2017, 12, 31, 23, 00, 00)}})
    print u'простая маленькая выборка ', smallVarFromMongo.count()


@timeit
def simpleSmallListOfDicts():
    list = []
    smallVarFromMongo = events.find({u'severity': u'1', u'params.admStatus': u'0', u'code': u'1.1.1.6.11',
                                     u'created': {u'$gt': datetime.datetime(2017, 12, 31, 23, 00, 00)}})
    for items in smallVarFromMongo:
        list.append(items)
    print u'кол-во словарей в списке простая маленькая выборка: ', len(list)


@timeit
def simpleBigCount():
    bigVarFromMongo = events.find({u'severity': u'0', u'params.admStatus': u'0', u'code': u'1.1.1.6.11',
                                   u'created': {u'$gt': datetime.datetime(2017, 05, 21, 12, 30, 00)}})
    print u'простая большая выборка ', bigVarFromMongo.count()


@timeit
def simpleBigListOfDicts():
    list = []
    bigVarFromMongo = events.find({u'severity': u'0', u'params.admStatus': u'0', u'code': u'1.1.1.6.11',
                                   u'created': {u'$gt': datetime.datetime(2017, 05, 21, 12, 30, 00)}})
    for items in bigVarFromMongo:
        list.append(items)
    print u'кол-во словарей в списке простая большая выборка: ', len(list)


@timeit
def complexBigCount():
    bigVarFromMongo = events.find(
        {u'category': u"3", u'created': {u'$gt': datetime.datetime(2017, 05, 1),
                                         u'$lt': datetime.datetime(2017, 10, 31)}, u'code': u'1.1.1.9',
         u'params.services': u"0", u'sourceType': u"0", u"code": u"1.1.1.9"})
    print u'кол-во словарей в сложной большая выборке', bigVarFromMongo.count()

@timeit
def complexBigListOfDicts():
    list = []
    bigVarFromMongo = events.find(
        {u'category': u"3", u'created': {u'$gt': datetime.datetime(2017, 05, 1),
                                         u'$lt': datetime.datetime(2017, 10, 31)}, u'code': u'1.1.1.9',
         u'params.services': u"0", u'sourceType': u"0", u"code": u"1.1.1.9"})
    for items in bigVarFromMongo:
        list.append(items)
    print u'кол-во словарей в списке сложная большая выборка: ', len(list)

@timeit
def totalTime():
    """total time: 99466 ms"""
    simpleSmallCount()
    simpleSmallListOfDicts()
    simpleBigCount()
    simpleBigListOfDicts()
    print u'end of total time func'
    client.close()


if __name__ == '__main__':
    complexBigCount()
    complexBigListOfDicts()
