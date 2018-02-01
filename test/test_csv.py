# -*- coding: UTF-8 -*-
import csv
import pprint
import codecs
import testDictWriter as dictWrite
import anotherDictWriter as aDictWrite
from pymongo import MongoClient
from vars_for_classes import generationEvents as gen
import pandas as pd
import json

FILENAME = "result.csv"
FIELDNAMESFORCSV = ('category','code','sourceType','created','sourceId','description','params','severity')
dictForCsv = {}
dictForCsv = gen()
listOfValue = []
with codecs.open(FILENAME, 'w') as fp:
    w = dictWrite.UnicodeDictWriter(fp, FIELDNAMESFORCSV)
    # w = csv.writer(fp, FIELDNAMESFORCSV)
    w.writeheader()
    for i in xrange(12):
        dictForCsv = gen()
        w.writerow(dictForCsv)
        if i % 1000 == 0:
            print u'записано в csv: {} событий'.format(i)


try:  # подключение к бд
    client = MongoClient('192.168.62.129', 27017)
    db = client.Events1
    events = db.Events1
    events.delete_many({})
except Exception as e:
    print e
    client.close()
try:
    with open('result.csv', 'r') as fp:
        r = csv.DictReader(fp)
        for row in r:
            print row
            db.Events1.insert(row)
finally:
    client.close()
    # print x
    # dictForMongo = {}
    # for word in x:
    #     dictForMongo[word] = None
    # dictKey = (k for k in dictForMongo.keys())
    # print dictForMongo.keys()
    # y = r.next()
    # for item in y:
    #    dictForMongo[dictKey.next()] = item
    # print dictForMongo
