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

@timeit
def main(cursor):
    with open('result.csv', 'rb') as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            dictOfParams = {}
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
            statement = '''insert into "Events" ("code", "created","sourcetype", "sourceid" , "category", "severity", "description", "params") values (%s,%s,%s,%s,%s,%s,%s,%s) returning "event_id"'''
            cursor.execute(statement, (
            row[u"code"], row[u"created"], row[u"sourceType"], row[u"sourceId"], row[u"category"], row[u"severity"],
            row[u"description"], row[u"params"]))
            id_ = cursor.fetchall()
            if id_[0]['event_id'] % 1000 == 0:
                print id_
            else:
                continue

if __name__ == '__main__':
    vars = [u'created', u'code', u'category', u'sourceType', u'sourceId', u'severity', u'description']
    # atttrs = [u'code', u'created',u'sourceType', u'sourceId' , u'category', u'severity', u'description', u'params']
    try:
        conn = psycopg2.connect(
            host='192.168.62.129',
            user='postgres',
            port=5432,
            password='qwe123',
            dbname='Events',
            client_encoding='utf-8')
        psycopg2.extras.register_hstore(conn, globally=False, unicode=False)
        conn.autocommit = True
        # cursor = conn.cursor()
        cursor = psycopg2.extras.RealDictCursor(conn)
        statement = '''CREATE TABLE "Events" (
                       event_id SERIAL,
                       code varchar(50),
                       created date,
                       sourceType varchar(50),
                       sourceId varchar(50),
                       category varchar(50),
                       severity varchar(50),
                       description varchar(50),
                       params hstore
                       );'''
        # for header in vars():
        #     statement = statement + '\n{} varchar(100),'.format(header)
        # statement = statement[:-1] + ');',
        cursor.execute(statement)
        # conn.commit()
        main(cursor)
    except Exception as e:
        print e
        conn.close()
    finally:
        print 'finally'
        conn.close()