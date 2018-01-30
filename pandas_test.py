# -*-coding: utf-8 -*-
import datetime
import pprint

import pandas as pd
from pymongo import MongoClient
from vars_for_classes import generationEvents as gen
import json
from bson import json_util


def myconverter(o): #to convert data in str
    if isinstance(o, datetime.datetime):
        return o.__str__()


FILENAME = 'result.json'
with open(FILENAME, 'w') as fp:
    dictFromClass = gen()
    df = pd.DataFrame.from_dict(dictFromClass, orient='index')
    dump = json.dump(df.to_dict(), fp, default=myconverter)

try:
    client = MongoClient('192.168.62.129', 27017)
    db = client.Events
    events = db.Events
    events.delete_many({})
except Exception as e:
    print e
    client.close()

eventsFromJson = open('result.json', 'r')
parsed = json.loads(eventsFromJson.read()) # <--- dict
dictForTest = {}
for v in parsed.values():
    dictForTest = v
    db.Events.insert(dictForTest)

eventsFromJson.close()
client.close()
