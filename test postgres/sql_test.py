# -*- coding: UTF-8 -*-
import csv
import datetime
import psycopg2.extras
import psycopg2
import sys, locale, re

reload(sys)
sys.setdefaultencoding('utf-8')
locale.setlocale(locale.LC_ALL, '')
vars = [u'created', u'code', u'category', u'sourceType', u'sourceId', u'severity', u'description']
# atttrs = [u'code', u'created',u'sourceType', u'sourceId' , u'category', u'severity', u'description', u'params']

try:
    conn = psycopg2.connect(
        host='192.168.62.129',
        user='postgres',
        port=5432,
        password='qwe123',
        dbname='testFromIdea',
        client_encoding='utf-8')
    psycopg2.extras.register_hstore(conn, globally=False, unicode=False)
    conn.autocommit = True
    # cursor = conn.cursor()
    cursor = psycopg2.extras.RealDictCursor(conn)
    # statement = '''CREATE TABLE "sql_dicts" (
    #                event_id SERIAL,
    #                code varchar(100),
    #                created date,
    #                sourceType varchar(100),
    #                sourceId varchar(100),
    #                category varchar(100),
    #                severity varchar(100),
    #                description varchar(100),
    #                params hstore
    #                );'''
    # # for header in vars():
    # #     statement = statement + '\n{} varchar(100),'.format(header)
    # # statement = statement[:-1] + ');',
    # cursor.execute(statement)
    # conn.commit()


    with open('result.csv', 'rb') as fp:
        dictOfParams = {}
        reader = csv.DictReader(fp)
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
            row[u'params'] = dictOfParams
            statement = '''insert into "sql_dicts" ("code", "created","sourcetype", "sourceid" , "category", "severity", "description", "params") values (%s,%s,%s,%s,%s,%s,%s,%s) returning "event_id"'''
            cursor.execute(statement, (row[u"code"], row[u"created"], row[u"sourceType"], row[u"sourceId"], row[u"category"], row[u"severity"],
                row[u"description"], row[u"params"]))
            id_ = cursor.fetchall()
            print id_[0][u'event_id']
finally:
    conn.close()
