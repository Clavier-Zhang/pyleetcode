from .cache import cache
from .config import urls, querys, SUCCESS, FAIL
from .system import system
from .screen import screen
import requests
import json
from bs4 import BeautifulSoup
import time

class Leetcode:

    session = requests.session()

    headers = {}

    def __init__(self):
        session_id = cache.get_user_session_id()
        csrf_token = cache.get_user_csrf_token()
        self.headers['Cookie'] = 'LEETCODE_SESSION=' + session_id + ';csrftoken=' + csrf_token + ';'
        self.headers['X-CSRFToken'] = csrf_token
        self.headers['Origin'] = urls['base']
        self.headers['Referer'] = urls['base']
        self.headers['X-Requested-With'] = 'XMLHttpRequest'

    # helper methods
    def post(self, url, data):
        return self.session.post(url, data=data, headers=self.headers)

    def get(self, url):
        return self.session.get(url, headers=self.headers)

    def get_cookie(self, cookies, attribute):
        cookies = str(cookies)
        start = cookies.index(attribute)+1+len(attribute)
        cookies = cookies[start:len(cookies)]
        start = cookies.index(' ')
        return cookies[0:start]
    
    def fetch_first_CSRFtoken(self):
        response = self.session.head(urls['login'])
        csrf_token = self.get_cookie(response.cookies, 'csrftoken')
        self.headers['Cookie'] = 'csrftoken=' + csrf_token + ';'
        return csrf_token

    # user methods
    def login(self, username, password):
        data = {
            'csrfmiddlewaretoken': self.fetch_first_CSRFtoken(),
            'login': username,
            'password': password
        }
        response = self.post(urls['login'], data)
        if (response.status_code != 200):
            cache.clear_user()
            return FAIL
        csrf_token = self.get_cookie(self.session.cookies, 'csrftoken')
        session_id = self.get_cookie(self.session.cookies, 'LEETCODE_SESSION')
        self.headers['Cookie'] = 'LEETCODE_SESSION=' + session_id + ';csrftoken=' + csrf_token + ';'
        self.headers['X-CSRFToken'] = csrf_token
        cache.save_session_and_token(session_id, csrf_token)
        return SUCCESS

    def logout(self):
        self.headers['Cookie'] = ''
        self.headers['X-CSRFToken'] = ''
        cache.clean()
        
    def fetch_all_questions(self):
        response = self.get(urls['all_questions'])
        if (response.status_code != 200):
            return FAIL
        cache.save_all_questions(response.json()['stat_status_pairs'])
        return SUCCESS

    def fetch_question_detail(self, titleSlug):
        data = {
            'query': querys['question_detail'],
            'variables': json.dumps({'titleSlug': titleSlug})
        }
        response = self.post(urls['graphql'], data=data)
        if (response.status_code != 200):
            return FAIL
        cache.save_question_detail(response.json()['data']['question'])
        return SUCCESS

    def submit(self, filename):
        data = {
            'lang': system.get_lang_from_filename(filename),
            'question_id': system.get_question_id_from_filename(filename),
            'typed_code': system.get_solution(filename),
        }
        response = self.post(urls['submit'], json.dumps(data))
        if (response.status_code != 200):
            return FAIL
        result = self.fetch_check_result(response.json()['submission_id'])
        screen.print_submit_result(result)
        return SUCCESS
    
    def test(self, filename):
        data = {
            'data_input': system.get_test_case(filename),
            'judge_type': "large",
            'lang': system.get_lang_from_filename(filename),
            'question_id': system.get_question_id_from_filename(filename),
            'typed_code': system.get_solution(filename),
        }
        response = self.post(urls['test'], json.dumps(data))
        if (response.status_code != 200):
            print(data)
            print(response.status_code)
            return FAIL
        test_result = self.fetch_check_result(response.json()['interpret_id'])
        expected_test_result = self.fetch_check_result(response.json()['interpret_expected_id'])
        screen.print_compare_test_result(test_result, expected_test_result)
        return SUCCESS

    def fetch_check_result(self, id):
        for count in range(0, 30):
            result = self.session.get(urls['check'].replace('$ID', str(id))).json()
            if (result['state'] == 'SUCCESS'):
                return result
            time.sleep(0.5)
        print('No response')
        return None

    def fetch_discussion_by_question_id(self, question_id):
        data = {
            'query': querys['discussion_list'],
            'variables': json.dumps({
                'orderBy': "most_votes", 
                'query': "", 'skip': 0, 
                'first': 20, 'tags': [], 
                'questionId': question_id
            }),
        }
        response = self.post(urls['graphql'], data=data).json()
        return response['data']['questionTopicsList']['edges']

    def fetch_discussion_post(self, post_id):
        data = {
            'query': querys['discussion_post'],
            'variables': json.dumps({'topicId': post_id}),
        }
        response = self.post(urls['graphql'], data=data).json()
        return response['data']['topic']


leetcode = Leetcode()