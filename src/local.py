import json
import os
import sys
import time

class Local:

    user = './data/user.json'
    path = os.path.dirname(os.path.abspath(__file__))+'/'
    token_valid_time = 10000

    def get_obj(self, filename):
        file = open(self.path+filename, 'r')
        obj = json.load(file)
        file.close()
        return obj

    def save_obj(self, filename, obj):
        file = open(self.path+filename, 'w')
        json.dump(obj, file)
        file.close()

    def fetch_user(self):
        return self.get_obj(self.user)

    def fetch_account_status(self):
        user = self.get_obj(self.user)
        if (user == None or type(user) != type(dict())):
            return False
        if ('username' not in user or 'password' not in user):
            return False
        if (user['username'] == '' or user['password'] == ''):
            return False
        return True

    def fetch_token_status(self):
        user = self.get_obj(self.user)
        if ('session_id' not in user or 'csrf_token' not in user):
            return False
        if (user['session_id'] == '' or user['csrf_token'] == ''):
            return False
        if (time.time() - user['login_time'] > self.token_valid_time):
            print('the token has expired')
            return False
        return True
        
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

    def clear_user(self):
        self.save_obj(self.user, {})

    def save_all_problems(self, problems):
        if (problems == None):
            return
        fp = open('./data/problems.json', 'w')
        json.dump(problems, fp)
        fp.close()

    def fetch_all_problems(self):
        return json.load(open('data/problems.json', 'r'))
