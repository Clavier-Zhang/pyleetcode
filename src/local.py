import json
import os
import sys
import time

class Local:

    path = os.path.dirname(os.path.abspath(__file__))+'/'

    user = './data/user.json'

    problems = './data/problems.json'

    token_valid_time = 3600*5

    problems_valid_time = 3600*24*7

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
        data = {
            'last_update_time': time.time(),
            'problems': problems,
        }
        self.save_obj(self.problems, data)

    def fetch_all_problems(self):
        return self.get_obj(self.path+self.problems)['problems']

    def fetch_problems_status(self):
        data = self.get_obj(self.path+self.problems)
        if (data == None or type(data) != type(dict())):
            return False
        if ('problems' not in data or len(data['problems']) == 0):
            return False
        if (time.time()-data['last_update_time'] > self.problems_valid_time):
            return False
        return True