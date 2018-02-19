# -*- coding: UTF-8 -*-
import csv
import datetime
import psycopg2.extras
import psycopg2
import sys, locale, re
from writing_to_db import timeit
from writing_to_db import writingToCsv
reload(sys)
sys.setdefaultencoding('utf-8')
locale.setlocale(locale.LC_ALL, '')

listOfShit = []
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

statement = '''select count(*) from "Events" where ("params" -> 'admStatus' like '%0%') and
                ("code" like '%1.1.1.6.11%') and ("severity" like '%1%') and
                ("created" > '2017-05-21 12:30:00')'''
cursor.execute(statement)

finded = cursor.fetchall()
print finded

statement = '''select * from "Events" where ("params" -> 'admStatus' like '%0%') and
                ("code" like '%1.1.1.6.11%') and ("severity" like '%1%') and
                ("created" > '2017-05-21 12:30:00')'''
cursor.execute(statement)
finded_ = cursor.fetchall()
# print finded_
for item in finded_:
    listOfShit.append(item)

print len(listOfShit)

