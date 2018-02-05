# -*- coding: utf-8 -*-

import csv
import pprint
import sys, locale, re

import datetime

reload(sys)
sys.setdefaultencoding('utf-8')
locale.setlocale(locale.LC_ALL, '')

FIELDNAMESFORCSV = (
    u'category', u'code', u'sourceType', u'created', u'sourceId', u'description', u'severity', u'segment',
    u'services', u'operation', u'zcName', u'ccName', u'operStatus', u'errorMsg', u'segment', u'unitName', u'unitType',
    u'dsName', u'dsType', u'objName', u'className', u'admStatus', u'softName', u'familyName', u'lName', u'lType',
    u'netName', u'personName', u'message', u'postName', u'personStatus', u'workGUI', u'docName', u'docType',
    u'contentName', u'actionType', u'message', u'metaName', u'taskName')
FILECSV = 'result.csv'

vars = [u'created', u'code', u'category', u'sourceType', u'sourceId', u'severity', u'description']

# def temp(numbers):
with open('result.csv', 'rb') as fp:
    dictOfParams = {}
    reader = csv.DictReader(fp)
    dict_list = []
    for row in reader:
        for k, v in row.items():
            if k not in vars:
                if v != '':
                    dictOfParams[k] = v
                    row.pop(k, None)
                else:
                    row.pop(k, None)
            elif k == u'created':
                date = row[u'created']
                row[u'created'] = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        row[u'params'] = dictOfParams
        pprint.pprint(row)
        print row
# temp(10)
