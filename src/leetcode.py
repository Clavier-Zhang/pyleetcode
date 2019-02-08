from .cache import Cache
import requests
import json
from bs4 import BeautifulSoup
import time

class Leetcode:

    session = requests.session()
    cache = Cache()

    headers = {
        'Origin': 'https://leetcode.com',
        'Referer': 'https://leetcode.com',
        'X-Requested-With': 'XMLHttpRequest',
    }

    login_url = 'https://leetcode.com/accounts/login/'
    graphql_url = 'https://leetcode.com/graphql'
    submit_url = 'https://leetcode.com/problems/add-two-numbers/submit/'
    all_problems_url = 'https://leetcode.com/api/problems/algorithms/'
    test_url = 'https://leetcode.com/problems/add-two-numbers/interpret_solution/'
    check_url = 'https://leetcode.com/submissions/detail/$ID/check/'

    # helper methods
    def post(self, url, data):
        session_id = self.cache.get_user_session_id()
        csrf_token = self.cache.get_user_csrf_token()
        self.headers['Cookie'] = 'LEETCODE_SESSION=' + session_id + ';csrftoken=' + csrf_token + ';'
        self.headers['X-CSRFToken'] = csrf_token
        response = self.session.post(url, data=data, headers=self.headers)
        return response

    def get(self, url):
        session_id = self.cache.get_user_session_id()
        csrf_token = self.cache.get_user_csrf_token()
        self.headers['Cookie'] = 'LEETCODE_SESSION=' + session_id + ';csrftoken=' + csrf_token + ';'
        self.headers['X-CSRFToken'] = csrf_token
        response = self.session.get(url, headers=self.headers)
        return response

    def get_cookie(self, cookies, attribute):
        cookies = str(cookies)
        start = cookies.index(attribute)+1+len(attribute)
        cookies = cookies[start:len(cookies)]
        start = cookies.index(' ')
        return cookies[0:start]
    
    def fetch_first_CSRFtoken(self):
        response = self.session.head(self.login_url)
        return self.get_cookie(response.cookies, 'csrftoken')

    # user methods
    def login(self, username, password):
        CSRFtoken = self.fetch_first_CSRFtoken()
        self.headers['Cookie'] = 'csrftoken=' + CSRFtoken + ';'
        data = {
            'csrfmiddlewaretoken': CSRFtoken,
            'login': username,
            'password': password
        }
        response = self.session.post(self.login_url, data=data, headers=self.headers)
        if (response.status_code != 200):
            self.cache.clear_user()
            return False
        csrf_token = self.get_cookie(self.session.cookies, 'csrftoken')
        session_id = self.get_cookie(self.session.cookies, 'LEETCODE_SESSION')
        self.cache.save_session_and_token(session_id, csrf_token)
        return True
        
    def get_user_info(self):
        data = {
            'query': '\n'.join([
                '{',
                '  user {',
                '    username',
                '    isCurrentUserPremium',
                '  }',
                '}'
            ]),
            'variables': {}
        }
        response = self.session.post(self.graphql_url, data=data, headers=self.headers)
        
        print(response.json())
    
    def get_all_problems(self):
        response = self.get(self.all_problems_url)
        self.cache.save_all_questions(response.json()['stat_status_pairs'])

    def get_one_problem_by_title_slug(self, titleSlug):
        data = {
            'query': '''
                query questionData($titleSlug: String!) {
                    question(titleSlug: $titleSlug) {
                        questionId
                        title
                        content
                        difficulty
                        likes
                        dislikes
                        status
                        similarQuestions
                        topicTags {
                            name
                            slug
                        }
                        codeSnippets {
                            lang
                            langSlug
                            code
                        }
                        sampleTestCase
                    }
                }
            ''',
            'variables': json.dumps({'titleSlug': titleSlug})
        }
        response = self.post(self.graphql_url, data=data)
        self.cache.save_question_detail(response.json()['data']['question'])

    def submit(self, filename):
        data = {
            'lang': filename[filename.index('.')+1:len(filename)],
            'question_id': filename[0:filename.index('-')],
            'typed_code': open(filename,'r').read()
        }
        response = self.post(self.submit_url, json.dumps(data)).json()
        print(response)
        result = self.fetch_check_result(response['submission_id'])
        print(result)
        return response
    
    def test(self, filename):
        data = {
            'data_input': "[2,4,3]\n[5,6,4]",
            'judge_type': "large",
            'lang': filename[filename.index('.')+1:len(filename)],
            'question_id': filename[0:filename.index('-')],
            'typed_code': open(filename,'r').read()
        }
        response = self.post(self.test_url, json.dumps(data)).json()
        result = self.fetch_check_result(response['interpret_id'])
        expected_result = self.fetch_check_result(response['interpret_expected_id'])
        print(result)
        print(expected_result)

    def fetch_check_result(self, id):
        count = 0
        while count < 10:
            result = self.session.get(self.check_url.replace('$ID', str(id))).json()
            if (result['state'] == 'SUCCESS'):
                return result
            time.sleep(0.5)
            count += 1
        print('No response')
        return None
        


