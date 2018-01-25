import random


class Test(object):

    def __init__(self):

        self.a = random.randint(1, 3)
        self.b = [2,3,4]

    def _message(self):

        attrs = [x for x in dir(self) if not x.startswith('_') and x != 'message']
        event_dict = {}
        for attr in attrs:
            event_dict[attr] = getattr(t, attr)
        return event_dict

t = Test()

print (t._message())