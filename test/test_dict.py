# -*- coding: utf-8 -*-

import datetime

import json
import pprint

from pymongo import MongoClient

from vars_for_classes import generationEvents

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

def dateToSting(dateFromClass):  # функция для json.dump что бы преобразовать дату в стринг
    if isinstance(dateFromClass, datetime.datetime):
        return dateFromClass.__str__()

def writingJson(numbers):
    """запись данных в 10 json файлов"""
    dictForJson = {}
    # for file_ in listOfFiles:
    with open(FILENAME0, 'w') as fp:
        listOfDicts = []
        for i in xrange(numbers):
            dictFromClass = generationEvents()
            listOfDicts.append(dictFromClass)
            if i % 1000 == 0:
                print u'прошло {} генераций события и записи в {}'.format(i, FILENAME0)
        dictForJson['A'] = listOfDicts
        json.dump(dictForJson, fp, default=dateToSting)


def writingMongoFromJson():
    """чтение 10 json файлов и запись их в бд"""
    try:
        # try:
        #     client = MongoClient('192.168.62.129', 27017)
        #     db = client.Events1
        #     events = db.Events1
        #     events.delete_many({})  # стирает записи из бд!!!
        # except Exception as e:
        #     print e
        #     client.close()
        for file__ in listOfFiles:
            with open(FILENAME0, 'r') as fp:
                print u'открыт {}'.format(FILENAME0)
                parsed = json.loads(fp.read())  # <--- dict
                for dictForMongo in parsed.values():  # parsed.values возвращает лист словарей,
                    # проход по этому листу и вытягивание одного словаря
                    # print type(dictForMongo)
                    listOfDicts = []
                    for item in dictForMongo:
                        # print type(item)
                        date = item['created']
                        # print date
                        item['created'] = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                        listOfDicts.append(item)
                        print type(item)
                        print type(listOfDicts)
                        for item_ in listOfDicts:
                            print item_
    except Exception as e:
        print e
    # finally:
    #     client.close()

if __name__ == '__main__':
    writingJson(15)
    writingMongoFromJson()