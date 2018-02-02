# -*- coding:utf-8 -*-

"""
Модуль для эксперементов + набор полезных приёмов.
"""

import sys, locale, re
reload(sys)
sys.setdefaultencoding('utf-8')
locale.setlocale(locale.LC_ALL, '')
print sys.getdefaultencoding()

import sys
import time
import datetime
import json


# тест скорости datetime
if 0:
    
    timestamp = time.mktime(datetime.datetime.now().timetuple())
    dt_str    = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    #print timestamp
    #print dt_str
    #datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')       
    
    count = 10**7
    
    t11 = time.clock()
    for i in xrange(count):
        datetime.datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')       
    t12 = time.clock()
    
    t21 = time.clock()
    for i in xrange(count):
        datetime.datetime.fromtimestamp(timestamp)  
    t22 = time.clock()
    
    print t12 - t11
    print t22 - t21
    print (t12 - t11) - (t22 - t21) 
    print (t12 - t11) / (t22 - t21) 
    
    sys.exit()

# start from there #######################################################################################################################

keys   = ['gen_id', 'created', 'source_id', 'oper_status', 'errorMsg', 'ccName']
params = set(['oper_status', 'errorMsg', 'lineName', 'ccName'])

filds_types = {'gen_id'      : int,
               'created'     : lambda x: datetime.datetime.fromtimestamp(float(x)),
               'source_id'   : unicode,
               'oper_status' : int,
               'errorMsg'    : unicode,
               'ccName'      : unicode}

def gen_dt():
    d = datetime.datetime.now()
    timestamp = time.mktime(d.timetuple())
    return timestamp

event1 = {'created' : gen_dt(), 'gen_id' : 1, 'source_id' : 'Источник данных 1', 'params' : {'oper_status' : 2, 'errorMsg' : 'Нет связи с сервером'}}
event2 = {'created' : gen_dt(), 'gen_id' : 2, 'source_id' : 'Источник данных 2', 'params' : {'oper_status' : 0, 'ccName' : 'УС Алмаз'}}
events = [event1, event2]

with open('out.csv', 'w') as f:
    buf_str = ';'.join(keys) + '\n'
    f.write(buf_str)
    for event in events:
        buf_list = []
        for key in keys: 
            if key in params:
                buf_list.append(str(event['params'].get(key, '')))
            else:
                buf_list.append(str(event[key]))
        buf_str = ';'.join(buf_list) + '\n'
        f.write(buf_str)

with open('out.csv', 'r') as f: date = f.read()
#print(date)

title_keys = []
with open('out.csv', 'r') as f:
    for new_line in f:
        if not new_line: break
        values = new_line.split(';')
        values.pop(-1)
        if not title_keys: title_keys = values; continue
        event = {'params' : {}}
        for number, key in enumerate(title_keys):
            value = values[number]
            value = filds_types[key](value)
            if key in params: event['params'][key] = value
            else:             event[key] = value
        print event
        
# end temp #######################################################################################################################

print 'done'
