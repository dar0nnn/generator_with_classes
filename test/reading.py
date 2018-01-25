# -*- coding: utf-8 -*-
import datetime
import multiprocessing as mp
import random
import time

from objectEvent import GoodEvent, BadEvent, UselessEvent
from pymongo import MongoClient


def read(qe, events):
    start_time = time.clock()  # старт отчета в секундах с вызова функции
    print('Started to writing in Mongo ',
          datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d::%H:%M:%S'))
    try:
        while True:
            # словарь-пустышка
            instance_dict = {'name': None, 'date': None, 'id_in_memory': None, 'code': None, 'message': None,
                             'time_created': 0}
            instance = qe.get_nowait()  # вытаскиваем инстанс
            # кортеж в список для удобства + append количества времени создания инстанса
            instance_message = list(instance.message())
            instance_message.append(instance.time_created())
            for num, k in enumerate(instance_dict.keys()):  # цикл для записи списка в словарь
                instance_dict[k] = instance_message[num]
            events.insert_one(instance_dict)  # вставка в бд
    except Exception as e:
        print(e)
    finally:
        client.close()
        t = time.clock() - start_time
        print(t / 60, 'minutes in reading thread')  # время выполнения потока


def gen(qe, numbers):
    n = 0
    start_time = time.clock()
    print('Start generating instances ',
          datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d::%H:%M:%S'))
    while n < numbers:  # генерация рандомных инстансов заданного количества
        rand = random.randint(1, 3)
        if rand == 1:
            instance = GoodEvent()
        elif rand == 2:
            instance = BadEvent()
        elif rand == 3:
            instance = UselessEvent()
        n += 1
        qe.put(instance)
    t = time.clock() - start_time
    print(t / 60, 'minutes in generating thread')  # время выполенения потока


if __name__ == '__main__':
    mp.set_start_method('spawn')
    try:
        client = MongoClient('192.168.62.129', 27017)  # подключение к бд
        db = client.Events1  # выбор базы Events
        events = db.Events1  # выбор коллекци Events
        events.delete_many({})  # очистка коллекции от записи
    except Exception as e:
        print(e)
    start_time = time.clock()
    print('Starting programm ', datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d::%H:%M:%S'))
    qe = mp.Queue()
    g = mp.Process(target=gen, args=(qe, 100000))
    r = mp.Process(target=read, args=(qe, events))
    g.start()
    r.start()
    print(time.clock() - start_time, 'seconds from main after generator.join()')
    print(time.clock() - start_time, 'seconds from main after reading.join()')
    print('Programm stopped: ', datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d::%H:%M:%S'))
