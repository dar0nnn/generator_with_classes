# -*- coding: UTF-8 -*-
import csv
import pghstore
import datetime
import json
import psycopg2.extras
import psycopg2
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
cursor = conn.cursor()
psycopg2.extras.register_hstore(conn)
try:
    # statement = '''CREATE TABLE sql_test_dicts (
    #                event_id SERIAL,
    #                code varchar(100),
    #                created date,
    #                sourceType varchar(100),
    #                sourceId varchar(100),
    #                category varchar(100),
    #                severity varchar(100),
    #                description varchar(100),
    #                value hstore
    #                );'''
    # for header in vars():
    #     statement = statement + '\n{} varchar(100),'.format(header)
    # statement = statement[:-1] + ');',
    # cursor.execute(statement)
    # conn.commit()


    with open('result.csv', 'rb') as fp:
        dictOfParams = {}
        reader = csv.DictReader(fp)
        for row in reader:
            listOfKeys = []
            listOfValues = []
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
            row[u'params'] = dictOfParams
            for k, v in row.items():
                listOfKeys.append(k)
                listOfValues.append(v)
            # print listOfKeys
            # print listOfValues

            statement = '''insert into "sql_test_dicts" ("code") values ('') returning "event_id"'''
            cursor.execute(statement)
            conn.commit()
            id_ = cursor.fetchall()
            print id_[0][0]

            for i in xrange(len(listOfKeys)):
                if type(listOfValues[i]) is dict:
                    forHstore = pghstore.dumps(listOfValues[i])
                    # listForHstore = []
                    # listForHstoreValues= []
                    # for k,v in listOfValues[i].items():
                    #     listForHstore.append(k)
                    #     listForHstore.append(v)
                    statement = '''update "sql_test_dicts" set ({}) = ('{}') where "event_id" = {} '''.format(listOfKeys[i], forHstore, id_[0][0])
                else:
                    statement = '''update "sql_test_dicts" set ({}) = ('{}') where "event_id" = {} '''.format(listOfKeys[i], listOfValues[i], id_[0][0])
                cursor.execute(statement)
                conn.commit()

            # statement = '''insert into "sql_test_dicts" {} values '{}' '''.format(tuple(listOfKeys), tuple(listOfValues))
            # cursor.execute(statement)
            # conn.commit()
finally:
    conn.close()