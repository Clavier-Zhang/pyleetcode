import json

class Local:
    def test(self):
        obj = {'a' : 'b', 'c' : 'd'}
        fp = open('./data/user.json', 'w')
        json.dump(obj, fp)
        fp.close()
        print(json.dumps(obj))
        print(json.load(open('./data/user.json', 'r')))


l = Local()
l.test()