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
        print(u'%r  %2.2f s' % (method.__name__, (te - ts)))
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
def complexSmallCount():
    smallVarFromMongo = events.find(
        {u'category': u'3', u'created': {u'$gt': datetime.datetime(2017, 05, 2),
                                         u'$lte': datetime.datetime(2017, 05, 24)},
         u'$and': [{u'sourceType': u'2'}, {u'sourceId': u'дополнительный сегмент'}],
         u'$or': [{u'code': u'1.1.2.6.5'}, {u'code': u'1.1.2.6.6'}], u'severity': u'2',
         u'$and': [{u'params.lType': u'0'},
                   {u'params.operStatus': u'3'}, {u'params.segment': u'0'}]})
    print u'сложная маленькая выборка: ', smallVarFromMongo.count()


@timeit
def complexSmallListOfDicts():
    list = []
    bigVarFromMongo = events.find(
        {u'category': u'3', u'created': {u'$gt': datetime.datetime(2017, 05, 2),
                                         u'$lte': datetime.datetime(2017, 05, 24)},
         u'$and': [{u'sourceType': u'2'}, {u'sourceId': u'дополнительный сегмент'}],
         u'$or': [{u'code': u'1.1.2.6.5'}, {u'code': u'1.1.2.6.6'}], u'severity': u'2',
         u'$and': [{u'params.lType': u'0'},
                   {u'params.operStatus': u'3'}, {u'params.segment': u'0'}]})
    for items in bigVarFromMongo:
        list.append(items)
    print u'кол-во словарей в списке сложная маленькая выборка: ', len(list)


@timeit
def complexBigCount():
    bigVarFromMongo = events.find(
        {u'category': u'1', u'created': {u'$gt': datetime.datetime(2017, 05, 1),
                                         u'$lte': datetime.datetime(2017, 10, 31)},
         u'$or': [{u'params.lType': u'0', u'params.operStatus': u'3', u'params.segment': u'0'}, {u'params.lType': u'2',
                                                                                                 u'params.operStatus': u'2',
                                                                                                 u'params.segment': u'1'}],
         u'sourceType': u"0",
         u'$or': [{u'code': u'1.1.2.6.5'}, {u'code': u'1.1.2.6.6'}]})
    print u'сложная большая выборка: ', bigVarFromMongo.count()


@timeit
def complexBigListOfDicts():
    list = []
    bigVarFromMongo = events.find(
        {u'category': u'1', u'created': {u'$gt': datetime.datetime(2017, 05, 1),
                                         u'$lt': datetime.datetime(2017, 10, 31)},
         u'$or': [{u'params.lType': u'0', u'params.operStatus': u'3', u'params.segment': u'0'}, {u'params.lType': u'2',
                                                                                                 u'params.operStatus': u'2',
                                                                                                 u'params.segment': u'1'}],
         u'sourceType': u"0",
         u'$or': [{u'code': u'1.1.2.6.5'}, {u'code': u'1.1.2.6.6'}]})
    for items in bigVarFromMongo:
        list.append(items)
    print u'кол-во словарей в списке сложная большая выборка: ', len(list)


@timeit
def regexSearch():
    smallVarFromMongo = events.find(
        {u'$or': [{u'category': u'1'}, {u'category': u'3'}],
         u'$and': [{u'sourceType': u'0'}, {u'sourceId': u'дополнительный сегмент'}],
         u'$or': [{u'code': u'1.1.2.6.5'}, {u'code': '1.1.2.6.6'}], u'severity': u'2',
         u'$and': [{u'params.lType': u'0'},
                   {u'params.operStatus': u'3'}, {u'params.lName': {u'$regex': u"лол"}}],
         u'$or': [{u'params.segment': u'0'}, {u'params.segment': u'1'}]})
    print u'поиск по тексту: ', smallVarFromMongo.count()


@timeit
def totalTime():
    simpleSmallCount()  # простая маленькая кол-во
    simpleSmallListOfDicts()  # простая маленькая в переменную
    simpleBigCount()  # простая большая кол-во
    simpleBigListOfDicts()  # простая большая в переменную
    complexSmallCount()  # сложная маленькая кол-во
    complexSmallListOfDicts()  # сложная маленькая в переменную
    complexBigCount()  # сложная большая кол-во
    complexBigListOfDicts()  # сложная большая в переменную
    regexSearch()  # поиск по фразе в тексте с кучей параметров
    print u'end of total time func'
    client.close()


if __name__ == '__main__':
    totalTime()
