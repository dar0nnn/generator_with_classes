# -*- coding: utf-8 -*-

import csv
import random
import sys, locale, re

import time

import datetime

reload(sys)
sys.setdefaultencoding('utf-8')
locale.setlocale(locale.LC_ALL, '')
from writing_to_db import  writingToCsv as csvWriter
from vars_for_classes import generationEvents
FIELDNAMESFORCSV = ('category','code','sourceType','created','sourceId','description','params','severity')
FILECSV = 'result.csv'



def temp(numbers):
    dictForCsv = {}
    with open(FILECSV, 'w') as fp:
        w = csv.DictWriter(fp, fieldnames=FIELDNAMESFORCSV)
        w.writeheader()
        for i in xrange(numbers):
            dictForCsv = generationEvents()
            w.writerow(dictForCsv)
            if i % 1000 == 0:
                print u'записано в csv: {} событий'.format(i)

# temp(10)
