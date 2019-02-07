import json

class Local:

    user = './data/user.json'

    def get_obj(self, filename):
        file = open(filename, 'r')
        obj = json.load(file)
        file.close()
        return obj

    def save_obj(self, filename, obj):
        file = open(filename, 'w')
        json.dump(obj, file)
        file.close()

    def save_session_and_token(self, session_id, csrf_token, login_time):
        user = self.get_obj(self.user)
        user['session_id'] = session_id
        user['csrf_token'] = csrf_token
        user['login_time'] = login_time
        self.save_obj(self.user, user)

    def save_username_and_password(self, username, password):
        user = self.get_obj(self.user)
        user['username'] = username
        user['password'] = password
        self.save_obj(self.user, user)

    def test(self):
        obj = {'a' : 'b', 'c' : None}
        lis = [1, 2, 3]
        
        fp = open('./data/user.json', 'w')
        json.dump(lis, fp)
        fp.close()
        print(json.load(open('./data/user.json', 'r')))

    def save_all_problems(self, problems):
        if (problems == None):
            return
        fp = open('./data/problems.json', 'w')
        json.dump(problems, fp)
        fp.close()

    def fetch_all_problems(self):
        return json.load(open('./data/problems.json', 'r'))

