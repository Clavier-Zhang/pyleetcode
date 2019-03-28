from .config import lang_dict
import json
import os
import time
from pathlib import Path
from src.data.company_tags import company_tags_data
from src.data.frequency import frequency_data

class Cache:

    user = 'data/user.json'

    question_index = 'data/question_index.json'

    question_details = 'data/question_details.json'

    frequency = 'data/frequency.json'

    company_tags = 'data/company_tags.json'

    token_valid_time = 3600*5

    question_index_valid_time = 3600*24*7

    question_list_capacity = 2001

    path = os.path.dirname(os.path.abspath(__file__))+'/'

    def __init__(self):
        if not Path(self.path+'data').is_dir():
            os.mkdir(self.path+'data')
        if not Path(self.path+self.user).is_file():
            open(self.path+self.user, 'w').write('{'+'}')
        if not Path(self.path+self.question_index).is_file():
            open(self.path+self.question_index, 'w').write('[]')
        if not Path(self.path+self.question_details).is_file():
            open(self.path+self.question_details, 'w').write('[]')

    # helper methods
    def get_obj(self, filename):
        file = open(os.path.dirname(os.path.abspath(__file__))+'/'+filename, 'r')
        obj = json.load(file)
        file.close()
        return obj

    def save_obj(self, filename, obj):
        file = open(os.path.dirname(os.path.abspath(__file__))+'/'+filename, 'w')
        json.dump(obj, file)
        file.close()

    # user cache methods
    def check_user_lang_status(self):
        user = self.get_obj(self.user)
        if ('lang' not in user):
            return False
        if (user['lang'] not in lang_dict):
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
        user = self.get_obj(self.user)
        if 'session_id' in user:
            return user['session_id']
        else:
            return ''
    
    def get_user_csrf_token(self):
        user = self.get_obj(self.user)
        if 'csrf_token' in user:
            return user['csrf_token']
        else:
            return ''

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
        data = self.get_obj(self.question_index)
        if ('problems' not in data or len(data['problems']) == 0):
            return False
        if (time.time()-data['last_update_time'] > self.question_index_valid_time):
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
        self.save_obj(self.question_index, data)

    def get_question_summarys_by_range(self, start, end):
        results = []
        problems = self.get_obj(self.question_index)['problems']
        for i in range(start, end+1):
            if problems[i] != None:
                results.append(problems[i])
        return results

    def get_question_summary_by_question_id(self, question_id):
        problems = self.get_obj(self.question_index)['problems']
        return problems[question_id]

    def get_question_detail_by_question_id(self, question_id):
        return self.get_obj(self.question_details)[question_id]

    def save_question_detail(self, question_detail):
        question_details = self.get_obj(self.question_details)
        if len(question_details) == 0:
            question_details = [None]*2000
        question_details[int(question_detail['questionId'])] = question_detail
        self.save_obj(self.question_details, question_details)

    def clean(self):
        open(self.path+self.user, 'w').write('{'+'}')
        open(self.path+self.question_index, 'w').write('[]')
        open(self.path+self.question_details, 'w').write('[]')

    def save_frequency(self, frequency_list):
        self.save_obj(self.frequency, frequency_list)

    def get_frequency_order_list(self):
        return frequency_data

    def save_company_tags(self, company_tags):
        self.save_obj(self.company_tags, company_tags)

    def get_company_tags(self):
        return company_tags_data

cache = Cache()