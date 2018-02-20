# -*- coding: UTF-8 -*-
import csv
import datetime
import pprint

import psycopg2.extras
import psycopg2
import sys, locale, re
from writing_to_db import timeit
from writing_to_db import writingToCsv
from findMongo import FindForTimeMongo

reload(sys)
sys.setdefaultencoding('utf-8')
locale.setlocale(locale.LC_ALL, '')


class FindForFindPostgres(FindForTimeMongo):
    def __init__(self, cursor):
        self.cursor = cursor

    @timeit
    def simpleSmallCount(self):
        statement = '''select count(*) from "Events" where
                       ("params" -> 'admStatus' like '%0%') and
                       ("code" like '%1.1.1.6.11%') and 
                       ("severity" like '%1%') and
                       ("created" > '2017-12-31 23:00:00')'''
        self.cursor.execute(statement)
        finded = self.cursor.fetchall()
        print u'простая маленькая выборка ', finded

    @timeit
    def simpleSmallListOfDicts(self):
        listOfFinded = []
        statement = '''select * from "Events" where 
                      ("params" -> 'admStatus' like '%0%') and
                      ("code" like '%1.1.1.6.11%') and 
                      ("severity" like '%1%') and
                      ("created" > '2017-12-31 23:00:00')'''
        self.cursor.execute(statement)
        finded = self.cursor.fetchall()
        for item in finded:
            listOfFinded.append(item)
        print u'кол-во словарей в списке простая маленькая выборка: ', len(listOfFinded)

    @timeit
    def simpleBigCount(self):
        statement = '''select count(*) from "Events" where 
                       ("params" -> 'admStatus' like '%0%') and
                       ("code" like '%1.1.1.6.11%') and 
                       ("severity" like '%1%') and 
                       ("created" > '2017-05-21 12:30:00')'''
        self.cursor.execute(statement)
        finded = self.cursor.fetchall()
        print u'простая большая выборка ', finded

    @timeit
    def simpleBigListOfDicts(self):
        listOfFinded = []
        statement = '''select * from "Events" where
                       ("params" -> 'admStatus' like '%0%') and
                       ("code" like '%1.1.1.6.11%') and
                       ("severity" like '%1%') and
                       ("created" > '2017-05-21 12:30:00')'''
        self.cursor.execute(statement)
        finded = self.cursor.fetchall()
        for item in finded:
            listOfFinded.append(item)
        print u'кол-во словарей в списке простая большая выборка: ', len(listOfFinded)

    @timeit
    def complexSmallCount(self):
        statement = '''select count(*) from "Events" where 
         ("category" like '%3%') and
         ("severity" like '%2%') and 
         (("created" > '2017-05-2') and 
          ("created" <= '2017-05-24')) and 
         (("sourcetype" like '%1%') and 
          ("sourceid" like '%дополнительный сегмент%')) and 
         (("params" -> 'lType' like '%0%') and 
          ("params" -> 'operStatus' like '%3%') and 
          ("params" -> 'segment' like '%0%')) and 
         (("code" like '%1.1.2.6.5%') or 
          ("code" like '%1.1.2.6.6%'));'''
        self.cursor.execute(statement)
        finded = self.cursor.fetchall()
        print u'сложная маленькая выборка: ', finded

    @timeit
    def complexSmallListOfDicts(self):
        listOfFinded = []
        statement = '''select * from "Events" where 
         ("category" like '%3%') and
         ("severity" like '%2%') and 
         (("created" > '2017-05-2') and 
          ("created" <= '2017-05-24')) and 
         (("sourcetype" like '%1%') and 
          ("sourceid" like '%дополнительный сегмент%')) and
         (("params" -> 'lType' like '%0%') and 
          ("params" -> 'operStatus' like '%3%') and 
          ("params" -> 'segment' like '%0%')) and
         (("code" like '%1.1.2.6.5%') or 
          ("code" like '%1.1.2.6.6%'));'''
        self.cursor.execute(statement)
        finded = self.cursor.fetchall()
        for item in finded:
            listOfFinded.append(item)
        print u'кол-во словарей в списке сложная маленькая выборка: ', len(listOfFinded)

    @timeit
    def complexBigCount(self):
        statement = '''select count(*) from "Events" where 
         ("category" like '%1%') and
         ("severity" like '%2%') and 
         (("created" > '2017-05-1') and ("created" <= '2017-10-31')) and 
          ("sourcetype" like '%0%') and
         ((("params" -> 'lType' like '%0%') and 
           ("params" -> 'operStatus' like '%3%') and 
           ("params" -> 'segment' like '%0%')) or 
          (("params" -> 'lType' like '%2%') and
           ("params" -> 'operStatus' like '%2%') and
           ("params" -> 'segment' like '%1%'))) and
         (("code" like '%1.1.2.6.5%') or 
          ("code" like '%1.1.2.6.6%'));'''
        self.cursor.execute(statement)
        finded = self.cursor.fetchall()
        print u'сложная большая выборка: ', finded

    @timeit
    def complexBigListOfDicts(self):
        listOfFinded = []
        statement = '''select * from "Events" where 
         ("category" like '%1%') and
         ("severity" like '%2%') and 
         (("created" > '2017-05-1') and ("created" <= '2017-10-31')) and 
          ("sourcetype" like '%0%') and
         ((("params" -> 'lType' like '%0%') and 
           ("params" -> 'operStatus' like '%3%') and 
           ("params" -> 'segment' like '%0%')) or 
          (("params" -> 'lType' like '%2%') and
           ("params" -> 'operStatus' like '%2%') and
           ("params" -> 'segment' like '%1%'))) and
         (("code" like '%1.1.2.6.5%') or 
          ("code" like '%1.1.2.6.6%'));'''
        self.cursor.execute(statement)
        finded = self.cursor.fetchall()
        for item in finded:
            listOfFinded.append(item)
        print u'кол-во словарей в списке сложная большая выборка: ', len(listOfFinded)

    @timeit
    def totalTime(self):
        self.simpleSmallCount()
        self.simpleSmallListOfDicts()
        self.simpleBigCount()
        self.simpleBigListOfDicts()
        self.complexSmallCount()
        self.complexSmallListOfDicts()
        self.complexBigCount()
        self.complexBigListOfDicts()
        print 'end of total time func'


if __name__ == '__main__':
    conn = psycopg2.connect(
        host='192.168.62.129',
        user='postgres',
        port=5432,
        password='qwe123',
        dbname='Events',
        client_encoding='utf-8')
    psycopg2.extras.register_hstore(conn, globally=False, unicode=False)
    conn.autocommit = True
    cursor = psycopg2.extras.RealDictCursor(conn)

    find = FindForFindPostgres(cursor=cursor)
    find.totalTime()
