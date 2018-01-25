# -*- coding: utf-8 -*-
import Queue
from threading import Thread
import time
import datetime
from objectEvent import GoodEvent, BadEvent, UselessEvent
import random
from pymongo import MongoClient


def timeit(method):  # замер времени
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result
    return timed


class ReadingQueue(Thread):
    """поток для чтения событий из очереди"""

    def __init__(self, qe):
        Thread.__init__(self)
        self.qe = qe

    @timeit
    def run(self):
        print('Started to writing in Mongo ',
              datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d::%H:%M:%S'))
        try:
            client = MongoClient('192.168.62.129', 27017)  # подключение к бд
            db = client.Events  # выбор базы Events
            events = db.Events  # выбор коллекци Events
            events.delete_many({})  # очистка коллекции от записи
            if self.qe.empty() == False:
                while not self.qe.empty():
                    # словарь-пустышка
                    instance_dict = {'name': None, 'date': None, 'id_in_memory': None, 'code': None, 'message': None,
                                     'time_created': 0}
                    instance = self.qe.get_nowait()  # вытаскиваем инстанс
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


class GeneratingEvents(Thread):
    """поток, генериующий инстансы классов для создания события"""

    def __init__(self, qe, numbers):
        Thread.__init__(self)
        self.qe = qe  # queue
        self.numbers = numbers  # количество классов, которое нужно создать

    @timeit
    def run(self):
        n = 0
        print('Start generating instances ',
              datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d::%H:%M:%S'))
        while n < self.numbers:  # генерация рандомных инстансов заданного количества
            rand = random.randint(1, 3)
            if rand == 1:
                instance = GoodEvent()
            elif rand == 2:
                instance = BadEvent()
            elif rand == 3:
                instance = UselessEvent()
            n += 1
            self.qe.put_nowait(instance)


@timeit
def main(numbers):
    print('Starting programm ', datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d::%H:%M:%S'))
    qe = Queue.Queue()
    g = GeneratingEvents(qe, numbers)
    r = ReadingQueue(qe)
    g.start()
    r.start()
    g.join()
    r.join()
    print('Programm stopped: ', datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d::%H:%M:%S'))


if __name__ == '__main__':
    numbers = int(raw_input('Input number: '))
    main(numbers)
