# -*- coding: UTF-8 -*-
import csv
import json
import sys, locale, re

reload(sys)
sys.setdefaultencoding('utf-8')
locale.setlocale(locale.LC_ALL, '')

vars = [u'created', u'code', u'category', u'sourceType', u'sourceId', u'severity', u'description']
FILECSV = 'result.csv'
FILENAME0 = 'result0.json'
FILENAME1 = 'result1.json'
FILENAME2 = 'result2.json'
FILENAME3 = 'result3.json'
FILENAME4 = 'result4.json'
FILENAME5 = 'result5.json'
FILENAME6 = 'result6.json'
FILENAME7 = 'result7.json'
FILENAME8 = 'result8.json'
FILENAME9 = 'result9.json'
listOfFiles = (
    FILENAME0, FILENAME1, FILENAME2, FILENAME3, FILENAME4, FILENAME5, FILENAME6, FILENAME7, FILENAME8, FILENAME9)
FIELDNAMESFORCSV = (
    u'category', u'code', u'sourceType', u'created', u'sourceId', u'description', u'severity', u'segment',
    u'services', u'operation', u'zcName', u'ccName', u'operStatus', u'errorMsg', u'segment', u'unitName', u'unitType',
    u'dsName', u'dsType', u'objName', u'className', u'admStatus', u'softName', u'familyName', u'lName', u'lType',
    u'netName', u'personName', u'message', u'postName', u'personStatus', u'workGUI', u'docName', u'docType',
    u'contentName', u'actionType', u'message', u'metaName', u'taskName')


def writingCsvFromJson():
    with open('resulting.csv', 'w') as f:
        for file__ in listOfFiles:
            with open(file__, 'r') as fp:
                data = json.load(open(file__))
            writer = csv.DictWriter(f, fieldnames=FIELDNAMESFORCSV)
            writer.writeheader()
            dictForCsv = data
            for item in dictForCsv['A']:
                for k, v in item.items():
                    if k == u'params':
                        for key_, value_ in item[u'params'].items():
                            item[key_] = value_
                item.pop(u'params', None)
                writer.writerow(item)

if __name__ == '__main__':
    writingCsvFromJson()