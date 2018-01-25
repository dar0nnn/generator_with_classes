from abc import ABCMeta


class Test1():
    __metaclass__ = ABCMeta

    def __init__(self, test=None, asdasd=None):
        self.test = test
        self.asdasd = asdasd

class Test2(Test1):
    def __init__(self, aqw, *args, **kw):
        super(Test2, self).__init__(*args, **kw)
        self.aqw = aqw

    def message(self):
        dirOfVars = {}
        vars = [x for x in dir(self) if
                not x.startswith('_') and x != 'message']
        for var in vars:
            dirOfVars[var] = getattr(self, var)
        print dirOfVars


dirOfKw = {'test': 123, 'asdasd': 'hello'}

x = (key for key in dirOfKw.keys())
y = (value for value in dirOfKw.values())

t = Test2(aqw='das')


for i in range(0, 2):
    value = x.next()
    classvalue = y.next()
    t.__setattr__(value, classvalue)

t.message()
