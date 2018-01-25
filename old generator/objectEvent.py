# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
import time
import datetime


class PrettendToBeEvent(object):
    #общий класс Event`ов
    __metaclass__ = ABCMeta
    @abstractmethod
    def message(self):
        pass

    def time_created(self):
        t = time.clock()
        return str(round(t, 3))


class GoodEvent(PrettendToBeEvent):
    #хороший Event

    def __init__(self):
        PrettendToBeEvent.__init__(self)

    def message(self):
        hello_message = 'Я хороший, найди меня'
        date = datetime.datetime.now().replace(microsecond=0).isoformat()
        name = type(self).__name__
        code = 200
        return name, date, id(self), code, hello_message


class BadEvent(PrettendToBeEvent):
    #плохой Event

    def __init__(self):
        PrettendToBeEvent.__init__(self)

    def message(self):
        hello_message = 'Я плохой, лучше не находи меня'
        date = datetime.datetime.now().replace(microsecond=0).isoformat()
        name = type(self).__name__
        code = 404
        return name, date, id(self), code, hello_message


class UselessEvent(PrettendToBeEvent):
    #Бесполезный Event для общего шума

    def __init__(self):
        PrettendToBeEvent.__init__(self)

    def message(self):
        hello_message = 'А я просто бесполезный'
        date = datetime.datetime.now().replace(microsecond=0).isoformat()
        name = type(self).__name__
        code = 100
        return name, date, id(self), code, hello_message


if __name__ == '__main__':
    pass
