from .cache import Cache
from .config import urls
from .system import System
from .screen import Screen
import requests
import json
from bs4 import BeautifulSoup
import time


class Leetcode:

    session = requests.session()
    cache = Cache()
    system = System()
    screen = Screen()

    headers = {
        'Origin': 'https://leetcode.com',
        'Referer': 'https://leetcode.com',
        'X-Requested-With': 'XMLHttpRequest',
    }

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
        response = self.session.head(urls['login'])
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
        response = self.session.post(urls['login'], data=data, headers=self.headers)
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
        response = self.session.post(urls['graphql'], data=data, headers=self.headers)
        
        print(response.json())
    
    def get_all_problems(self):
        response = self.get(urls['all_problems'])
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
        response = self.post(urls['graphql'], data=data)
        self.cache.save_question_detail(response.json()['data']['question'])

    def submit(self, filename):
        data = {
            'lang': filename[filename.index('.')+1:len(filename)],
            'question_id': filename[0:filename.index('-')],
            'typed_code': self.system.get_solution(filename),
        }
        response = self.post(urls['submit'], json.dumps(data)).json()
        result = self.fetch_check_result(response['submission_id'])
        self.screen.print_submit_result(result)
    
    def test(self, filename):
        data = {
            'data_input': self.system.get_test_case(filename),
            'judge_type': "large",
            'lang': filename[filename.index('.')+1:len(filename)],
            'question_id': filename[0:filename.index('-')],
            'typed_code': self.system.get_solution(filename),
        }
        response = self.post(urls['test'], json.dumps(data)).json()
        test_result = self.fetch_check_result(response['interpret_id'])
        expected_test_result = self.fetch_check_result(response['interpret_expected_id'])
        self.screen.print_compare_test_result(test_result, expected_test_result)

    def fetch_check_result(self, id):
        count = 0
        while count < 30:
            result = self.session.get(urls['check'].replace('$ID', str(id))).json()
            if (result['state'] == 'SUCCESS'):
                return result
            time.sleep(0.5)
            count += 1
        print('No response')
        return None

    def fetch_discussion_by_question_id(self, question_id):
        data = {
            'query':"query questionTopicsList($questionId: String!, $orderBy: TopicSortingOption, $skip: Int, $query: String, $first: Int!, $tags: [String!]) {\n  questionTopicsList(questionId: $questionId, orderBy: $orderBy, skip: $skip, query: $query, first: $first, tags: $tags) {\n    ...TopicsList\n   }\n}\n\nfragment TopicsList on TopicConnection {\n  totalNum\n  edges {\n    node {\n      id\n      title\n      commentCount\n      viewCount\n     tags {\n        name\n        slug\n        }\n      post {\n        id\n        voteCount\n        creationDate\n        author {\n          profile {\n                  __typename\n          }\n          __typename\n        }\n        status\n        coinRewards {\n          ...CoinReward\n          __typename\n        }\n        __typename\n      }\n      lastComment {\n        id\n        post {\n          id\n          author {\n            username\n            profile {\n              userSlug\n              __typename\n            }\n            __typename\n          }\n          peek\n          creationDate\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    cursor\n    __typename\n  }\n  __typename\n}\n\nfragment CoinReward on ScoreNode {\n  id\n  score\n  description\n  date\n  __typename\n}\n",
            'variables': json.dumps({'orderBy': "most_votes", 'query': "", 'skip': 0, 'first': 20, 'tags': [], 'questionId': question_id}),
        }
        response = self.post(urls['graphql'], data=data).json()
        return response['data']['questionTopicsList']['edges']

    def fetch_decussion_post(self, post_id):
        data = {
            'query': 'query DiscussTopic($topicId: Int!) {\n  topic(id: $topicId) {\n    id\n    viewCount\n    topLevelCommentCount\n      title\n       post {\n      ...DiscussPost\n        }\n    }\n}\n\nfragment DiscussPost on PostNode {\n  id\n  voteCount\n  voteStatus\n  content\n    }\n \n',
            'variables': json.dumps({'topicId': post_id}),
        }
        response = self.post(urls['graphql'], data=data).json()
        return response['data']['topic']


