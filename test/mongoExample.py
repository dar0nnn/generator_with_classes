import datetime
from pymongo import MongoClient
import pprint

client = MongoClient('mongodb://localhost:27017/', )
db = client.unicorns
collection = db.unicorns

post = {"author": "Mike",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow()}
posts = db.posts

pprint.pprint(posts.find_one())
client.close()
