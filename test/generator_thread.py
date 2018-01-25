import random
from threading import Thread

from objectEvent import GoodEvent, BadEvent, UselessEvent


class GeneratingEvents(Thread):
    """класс для создания потока и генерации инстансов классов для создания события"""

    def __init__(self, qe, numbers):
        Thread.__init__(self)
        self.qe = qe  # queue
        self.numbers = numbers  # количество классов, которое нужно создать

    def run(self):
        n = 0
        while n < self.numbers:
            rand = random.randint(1, 3)
            if rand == 1:
                instance = GoodEvent()
            elif rand == 2:
                instance = BadEvent()
            elif rand == 3:
                instance = UselessEvent()
            n += 1
            self.qe.put_nowait(instance)
