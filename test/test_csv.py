# -*- coding: UTF-8 -*-
from pymongo import MongoClient
from bson import json_util
from vars_for_classes import generationEvents as gen
import pandas as pd
import json

FILENAME = "events.json"
listOfDict = []

se = pd.Series()
with open('result.csv', 'w') as fp:
    for i in xrange(100):
        df = pd.DataFrame.from_dict(gen())
        df.to_csv(columns='index')
        print i

try:  # подключение к бд
    client = MongoClient('192.168.62.129', 27017)
    db = client.Events
    events = db.Events
    events.delete_many({})
except Exception as e:
    print e
    client.close()
#
# eventsFromJson = open('result.json', 'r')
# parsed = json.loads(eventsFromJson.read())
#
# for item in parsed['records']:
#     db.Events.insert(item)
#
df = pd.read_csv(FILENAME, sep='\t', encoding='utf-8')

db.Events.insert_many(df.to_dict('records'))
