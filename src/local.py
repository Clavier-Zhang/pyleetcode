import json
import os
import sys
import time

class Local:

    user = './data/user.json'
    path = os.path.dirname(os.path.abspath(__file__))+'/'

    def get_obj(self, filename):
        file = open(self.path+filename, 'r')
        obj = json.load(file)
        file.close()
        return obj

    def save_obj(self, filename, obj):
        file = open(self.path+filename, 'w')
        json.dump(obj, file)
        file.close()

    def fetch_login_status(self):
        user = self.get_obj(self.user)
        print(time.time() > user['login_time'])
        if (user == None or type(user) != type(dict())):
            return False
        if ('username' not in user or 'password' not in user):
            return False
        if (user['username'] == '' or user['password'] == ''):
            return False
        if ('session_id' not in user or 'csrf_token' not in user):
            return False
        if (user['session_id'] == '' or user['csrf_token'] == ''):
            return False
        
    def save_session_and_token(self, session_id, csrf_token):
        user = self.get_obj(self.user)
        if (type(user) != type(dict())):
            user = {}
        user['session_id'] = session_id
        user['csrf_token'] = csrf_token
        user['login_time'] = time.time()
        self.save_obj(self.user, user)

    def save_username_and_password(self, username, password):
        user = self.get_obj(self.user)
        user['username'] = username
        user['password'] = password
        self.save_obj(self.user, user)

    def save_all_problems(self, problems):
        if (problems == None):
            return
        fp = open('./data/problems.json', 'w')
        json.dump(problems, fp)
        fp.close()

    def fetch_all_problems(self):
        return json.load(open('data/problems.json', 'r'))


l = Local()
print(l.get_obj('data/user.json'))