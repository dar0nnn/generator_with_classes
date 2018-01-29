# -*- coding: UTF-8 -*-
from pymongo import MongoClient
from bson import json_util
from vars_for_classes import generationEvents as gen
import pandas as pd
import json
from pandas.core.common import _maybe_box_datetimelike

listOfKeys = []
FILENAME = "events.json"
# for i in xrange(10000):
#     events = gen()
#     for k in events.keys():
#         listOfKeys.append(k)
#     df = pd.DataFrame.from_dict(events, orient='index')
#     df.to_csv(FILENAME,mode='a', sep='\t', encoding='utf-8')
#     print i
with open('result.json', 'w') as fp:
    for i in xrange(10000):
        events = gen()
        # for k in events.keys():
        #     listOfKeys.append(k)
        json.dump(events, fp, encoding='utf-8', default=json_util.default)
        print i

try:  # подключение к бд
    client = MongoClient('192.168.62.129', 27017)
    db = client.Events
    events = db.Events
    events.delete_many({})
except Exception as e:
    print e
    client.close()

eventsFromJson = open('result.json', 'r')
parsed = json.loads(eventsFromJson.read())

for item in parsed['records']:
    db.Events.insert(item)
#
# df = pd.read_csv(FILENAME, sep='\t', encoding='utf-8')
#
# db.Events.insert_many(df.to_dict('records'))
