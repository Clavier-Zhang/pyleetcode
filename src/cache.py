from .config import lang_dict
import json
import os
from pathlib import Path
import time
from src.data.company_frequency_ranking import company_frequency_ranking

class Cache:

    user = 'data/user.json'

    question_index = 'data/question_index.json'

    company_frequency_ranking = 'data/company_frequency_ranking.py'

    lru = 'data/lru.json'

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
        if not Path(self.path+self.lru).is_file():
            open(self.path+self.lru, 'w').write('[]')

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

    def save_str(self, filename, text):
        file = open(os.path.dirname(os.path.abspath(__file__))+'/'+filename, 'w')
        file.write(text)
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

    def clean(self):
        open(self.path+self.user, 'w').write('{'+'}')
        open(self.path+self.question_index, 'w').write('[]')
        open(self.path+self.question_details, 'w').write('[]')

    def question_id_to_question_slug(self, question_id):
        summary = self.get_question_summary_by_question_id(question_id)
        if summary == None:
            return None
        return self.get_question_summary_by_question_id(question_id)['stat']['question__title_slug']

    def save_company_frequency_ranking(self, obj):
        self.save_str(self.company_frequency_ranking, 'company_frequency_ranking = '+str(obj))

    def get_company_questions(self, company):
        return company_frequency_ranking[company]

    def get_company_slugs(self):
        return list(company_frequency_ranking.keys())

cache = Cache()