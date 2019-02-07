import json
import os
import sys
import time

class Local:

    path = os.path.dirname(os.path.abspath(__file__))+'/'

    user = './data/user.json'

    problems = './data/problems.json'

    problem_details = './data/problem_details.json'

    token_valid_time = 3600*5

    problems_valid_time = 3600*24*7

    langs = ['cpp', 'java', 'python', 'python3', 'c', 'csharp', 'javascript', 'ruby', 'swift', 'golang', 'scala', 'kotlin', 'rust', 'php']

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
        problem_list = [None]*2000
        for problem in problems:
            problem_list[problem['stat']['question_id']] = problem
        data = {
            'last_update_time': time.time(),
            'problems': problem_list,
        }
        self.save_obj(self.problems, data)

    def fetch_all_problems(self):
        return self.get_obj(self.problems)['problems']

    def fetch_problems_with_range(self, start, end):
        results = []
        problems = self.get_obj(self.problems)['problems']
        for i in range(start, end+1):
            results.append(problems[i])
        return results

    def fetch_problem_by_id(self, question_id):
        problems = self.get_obj(self.problems)['problems']
        return problems[question_id]

    def check_problems_status(self):
        data = self.get_obj(self.problems)
        if (data == None or type(data) != type(dict())):
            return False
        if ('problems' not in data or len(data['problems']) == 0):
            return False
        if (time.time()-data['last_update_time'] > self.problems_valid_time):
            return False
        return True

    def check_problem_details_status(self, question_id):
        data = self.get_obj(self.problem_details)
        if data == None or type(data) != type(list()):
            return False
        if (len(data) == 0):
            return False
        if data[question_id] == None:
            return False
        return True

    def save_one_problem_detail(self, problem_detail):
        problem_details = self.get_obj(self.problem_details)
        if problem_detail == None or type(problem_details) != type(list()):
            problem_details = [None]*2000
        problem_details[int(problem_detail['questionId'])] = problem_detail
        self.save_obj(self.problem_details, problem_details)

    def fetch_one_problem_detail(self, question_id):
        problem_details = self.get_obj(self.problem_details)
        return problem_details[question_id]

    def check_user_lang_status(self):
        user = self.get_obj(self.user)
        if (user == None or type(user) != type(dict())):
            return False
        if ('lang' not in user):
            return False
        if (user['lang'] not in self.langs):
            return False
        return True
    
    def save_user_lang(self, lang):
        user = self.get_obj(self.user)
        user['lang'] = lang
        self.save_obj(self.user, user)

    def fetch_user_lang(self):
        return self.get_obj(self.user)['lang']