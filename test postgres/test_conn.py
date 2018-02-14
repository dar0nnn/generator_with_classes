# -*- coding: UTF-8 -*-
import csv

import datetime
import psycopg2
import psycopg2.extras as dictCurs
import sys, locale, re

reload(sys)
sys.setdefaultencoding('utf-8')
locale.setlocale(locale.LC_ALL, '')

vars = [u'created', u'code', u'category', u'sourceType', u'sourceId', u'severity', u'description']
conn = psycopg2.connect(
    host='192.168.62.129',
    user='postgres',
    port=5432,
    password='qwe123',
    dbname='testFromIdea')

with open('result.csv', 'rU') as fp:
    dictOfParams = {}
    reader = csv.DictReader(fp)
    cursor = conn.cursor()
    for row in reader:
        for k, v in row.items():
            if k not in vars:
                if v != '':
                    dictOfParams[k] = v
                    row.pop(k, None)
                else:
                    row.pop(k, None)
            elif k == u'created':
                date = float(row[u'created'])
                row[u'created'] = datetime.datetime.fromtimestamp(date)
        # statement = 'create table testfromidea ('
        # for header in row.keys():
        #     statement = statement + '\n{} varchar(100),'.format(header)
        # statement = statement[:-1] + ');'
        # cursor.execute(statement)
        cols = tuple(row.keys())
        vals = tuple(row.values())
        # # [row[x] for x in cols]
        vals_str = str(vals)
        for i in cols:
            for j in vals:
                stringJ = tuple(str(j))
                cursor.execute("INSERT INTO testfromidea ({cols}) VALUES ({vals_str})".format(
                    cols=i, vals_str=stringJ))

    # для создания таблицы и полей в ней
    # statement = 'create table testFromIDEA ('
    #
    # for header in FIELDNAMESFORPOST:
    #     statement = statement + '\n{} varchar(100),'.format(header)

    # statement = statement[:-1] + ');'
