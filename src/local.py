import json

class Local:
    def test(self):
        obj = {'a' : 'b', 'c' : None}
        lis = [1, 2, 3]
        
        fp = open('./data/user.json', 'w')
        json.dump(lis, fp)
        fp.close()
        print(json.load(open('./data/user.json', 'r')))
    
    def save_all_problems(self, problems):
        if (problems == None) return
        fp = open('./data/problems.json', 'w')
        json.dump(problems, fp)
        fp.close()

    def fetch_all_problems(self):
        return json.load(open('./data/problems.json', 'r'))


l = Local()
l.test()