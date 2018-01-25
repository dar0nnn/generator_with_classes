import pprint


def test_func():
    t = 12
    name = 'Sir Alex'
    dif_name = 'Sir Nick \n fon Naiman'
    dict_struct = {'name': 'Sir Volfgan',
                   'number': 12,
                   'another struct': {13: 45, 'mafia': 'hi'}}
    return t, name, dif_name, dict_struct


def main():
    dir = {}
    name = 'qwe'
    dir[name] = test_func()
    pprint.pprint(dir)
    t, name, *etc = test_func()
    dir['another name'] = t, name
    pprint.pprint(dir)
    print(type(etc))
    print(etc[1]['another struct']['mafia'])

main()
