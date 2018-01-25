import pprint
from bson.code import Code
from pymongo import MongoClient


def connection_to_db():
    try:
        client = MongoClient('mongodb://localhost:27017/', username='daron',
                             password='12345678',
                             authSource='admin',
                             authMechanism='SCRAM-SHA-1')  # подключение к бд
        db = client.Events
        coll = db.Events
        # second_coll = db.diffEvents
        map = Code("function () {"
                   "  this.code.forEach(function(z) {"
                   "    emit(z, 1);"
                   "  });"
                   "}")
        reduce = Code("function (key, values) {"
                      "  var total = 0;"
                      "  for (var i = 0; i < values.length; i++) {"
                      "    total += values[i];"
                      "  }"
                      "  return total;"
                      "}")
        result = coll.map_reduce(map, reduce, "myresults")
        for doc in result.find():
            print(doc)
        for event in coll.find({'name': 'GoodEvent'}).sort([('date', 1)]).limit(5):
            pprint.pprint(event)
    except Exception as e:
        print(e)
    finally:
        client.close()


if __name__ == '__main__':
    connection_to_db()
