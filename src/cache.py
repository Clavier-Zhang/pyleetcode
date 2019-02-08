import json
import os
import sys
import time

class Cache:

    path = os.path.dirname(os.path.abspath(__file__))+'/'

    user = './data/user.json'

    problems = './data/problems.json'

    question_details = './data/question_details.json'

    token_valid_time = 3600*5

    problems_valid_time = 3600*24*7

    question_list_capacity = 2001

    langs = ['cpp', 'java', 'python', 'python3', 'c', 'csharp', 'javascript', 'ruby', 'swift', 'golang', 'scala', 'kotlin', 'rust', 'php']

    # helper methods
    def get_obj(self, filename):
        file = open(self.path+filename, 'r')
        obj = json.load(file)
        file.close()
        return obj

    def save_obj(self, filename, obj):
        file = open(self.path+filename, 'w')
        json.dump(obj, file)
        file.close()

    # user cache methods
    def check_user_lang_status(self):
        user = self.get_obj(self.user)
        if ('lang' not in user):
            return False
        if (user['lang'] not in self.langs):
            return False
        return True
    
    def check_user_account_statue(self):
        user = self.get_obj(self.user)
        if ('username' not in user or 'password' not in user):
            return False
        if (user['username'] == '' or user['password'] == ''):
            return False
        return True

    def check_user_token_statue(self):
        user = self.get_obj(self.user)
        if ('session_id' not in user or 'csrf_token' not in user):
            return False
        if (user['session_id'] == '' or user['csrf_token'] == ''):
            return False
        if (time.time() - user['login_time'] > self.token_valid_time):
            # gonna replace with screen printer
            print('the token has expired')
            return False
        return True

    def save_user_lang(self, lang):
        user = self.get_obj(self.user)
        user['lang'] = lang
        self.save_obj(self.user, user)

    def get_user_lang(self):
        return self.get_obj(self.user)['lang']

    def get_user_username(self):
        return self.get_obj(self.user)['username']

    def get_user_password(self):
        return self.get_obj(self.user)['password']
    
    def get_user_session_id(self):
        return self.get_obj(self.user)['session_id']
    
    def get_user_csrf_token(self):
        return self.get_obj(self.user)['csrf_token']

    def clear_user(self):
        self.save_obj(self.user, {})

    def save_session_and_token(self, session_id, csrf_token):
        user = self.get_obj(self.user)
        user['session_id'] = session_id
        user['csrf_token'] = csrf_token
        user['login_time'] = time.time()
        self.save_obj(self.user, user)

    def save_username_and_password(self, username, password):
        user = self.get_obj(self.user)
        user['username'] = username
        user['password'] = password
        self.save_obj(self.user, user)

    # question methods
    def check_question_index_status(self):
        data = self.get_obj(self.problems)
        if ('problems' not in data or len(data['problems']) == 0):
            return False
        if (time.time()-data['last_update_time'] > self.problems_valid_time):
            return False
        return True

    def check_question_detail_status_by_question_id(self, question_id):
        data = self.get_obj(self.question_details)
        if len(data) == 0:
            return False
        if data[question_id] == None:
            return False
        return True

    def save_all_questions(self, problems):
        problem_list = [None]*self.question_list_capacity
        for problem in problems:
            problem_list[problem['stat']['question_id']] = problem
        data = {
            'last_update_time': time.time(),
            'problems': problem_list,
        }
        self.save_obj(self.problems, data)

    def get_questions_with_range(self, start, end):
        results = []
        problems = self.get_obj(self.problems)['problems']
        for i in range(start, end+1):
            results.append(problems[i])
        return results

    def get_question_detail_by_question_id(self, question_id):
        problems = self.get_obj(self.problems)['problems']
        return problems[question_id]

    def save_question_detail(self, question_detail):
        question_details = self.get_obj(self.question_details)
        if len(question_details) == 0:
            question_details = [None]*2000
        question_details[int(question_detail['questionId'])] = question_detail
        self.save_obj(self.question_details, question_details)