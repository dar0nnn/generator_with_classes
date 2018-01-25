import pprint

import datetime
from pymongo import MongoClient

conn = MongoClient('mongodb://localhost:27017/')

db = conn.unicorns

unicorn = {"name": "Aurora",
           "gender": "f",
           'loves': ['carrot', 'papaya'],
           "date": datetime.datetime.utcnow()}

unicorns = db.unicorns
unicorn_id = unicorns.insert(unicorn)
for unicorn in unicorns.find():
    pprint.pprint(unicorn)
conn.close()