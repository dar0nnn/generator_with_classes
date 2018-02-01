# -*- coding: UTF-8 -*-
import pprint

import testDictWriter as dictWrite

from pymongo import MongoClient
from vars_for_classes import generationEvents as gen
import pandas as pd
import json

FILENAME = "result.csv"

dictForCsv = {}
dictForCsv = gen()
listOfValue = []
with open('result.csv', 'wb') as fp:
    dictKey = sorted(dictForCsv.keys())
    w = dictWrite.UnicodeDictWriter(fp, dictKey)
    w.writeheader()
    for i in xrange(12):
        for k in dictKey:
            itemfromdict = dictForCsv[k]
            listOfValue.append(itemfromdict)
        w.writerow(listOfValue)

def read_file_line_by_line(file_):
  with open(file_, 'r') as fp:
      while True:
        line = fp.readline()
        if not line:
          break
        yield line

try:  # подключение к бд
    client = MongoClient('192.168.62.129', 27017)
    db = client.Events1
    events = db.Events1
    events.delete_many({})
except Exception as e:
    print e
    client.close()
with open('result.csv', 'r') as fp:
    r = dictWrite.UnicodeReader(fp)
    x = r.next()
    print x
    dictForMongo = {}
    for word in x:
        dictForMongo[word] = None
    dictKey = (k for k in dictForMongo.keys())
    print dictForMongo.keys()
    y = r.next()
    for item in y:
       dictForMongo[dictKey.next()] = item
    print dictForMongo
