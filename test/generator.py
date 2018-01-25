import random
import threading

import queue
from objectEvent import GoodEvent, BadEvent, UselessEvent


def class_creating(q, numbers):
    """создание инстанса одного из трех объектов 'события'"""
    n = 0
    while n < numbers:
        rand = random.randint(1, 3)
        if rand == 1:
            instance = GoodEvent()
        elif rand == 2:
            instance = BadEvent()
        elif rand == 3:
            instance = UselessEvent()
        n += 1
        q.put_nowait(instance) #входит в очередь что бы выйти отсюда!


if __name__ == '__main__':
    qe = queue.Queue()
    t = threading.Thread(target=class_creating, args=[qe, 100000])
    t.start()

    while t.is_alive():
        class_in_thread = qe.get()
        print(class_in_thread.message())
#        message_from_thread = qe.get() #выходит из потока прямиком в вывод!!!
#        print(message_from_thread)
