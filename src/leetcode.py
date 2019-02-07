import requests
import json
from bs4 import BeautifulSoup
from .local import Local

class Leetcode:

    session = requests.session()
    local = Local()

    headers = {
        'Origin': 'https://leetcode.com',
        'Referer': 'https://leetcode.com',
        'X-Requested-With': 'XMLHttpRequest',
    }

    login_url = 'https://leetcode.com/accounts/login/'
    graphql_url = 'https://leetcode.com/graphql'
    submit_url = 'https://leetcode.com/problems/add-two-numbers/submit/'

    def get_cookie(self, cookies, attribute):
        cookies = str(cookies)
        start = cookies.index(attribute)+1+len(attribute)
        cookies = cookies[start:len(cookies)]
        start = cookies.index(' ')
        return cookies[0:start]
    
    def get_first_CSRFtoken(self):
        response = self.session.head(self.login_url)
        return self.get_cookie(response.cookies, 'csrftoken')

    def login(self, username, password):
        CSRFtoken = self.get_first_CSRFtoken()
        self.headers['Cookie'] = 'csrftoken=' + CSRFtoken + ';'
        data = {
            'csrfmiddlewaretoken': CSRFtoken,
            'login': username,
            'password': password
        }
        response = self.session.post(self.login_url, data=data, headers=self.headers)
        if (response.status_code != 200):
            self.local.clear_user()
            raise Exception('Fail to login')
        csrf_token = self.get_cookie(self.session.cookies, 'csrftoken')
        session_id = self.get_cookie(self.session.cookies, 'LEETCODE_SESSION')

        self.local.save_session_and_token(session_id, csrf_token)
        
        self.headers['Cookie'] = 'LEETCODE_SESSION=' + session_id + ';csrftoken=' + csrf_token + ';'
        self.headers['X-CSRFToken'] = csrf_token

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
        data = {
            'query': '''
                query allQuestions {
                    allQuestions {
                        ...questionSummaryFields
                    }
                }
                fragment questionSummaryFields on QuestionNode {
                    title
                    titleSlug
                    questionId
                    status
                    difficulty
                    isPaidOnly
                }
                ''',
            'variables': {}
        }
        response = self.session.post(self.graphql_url, data=data, headers=self.headers)
        for q in response.json()['data']['allQuestions']:
            print(q)
        # print(response.json()['data']['allQuestions'])

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
                        status
                        sampleTestCase
                    }
                }
            ''',
            'variables': json.dumps({'titleSlug': titleSlug})
        }
        response = self.session.post(self.graphql_url, data=data, headers=self.headers)
        print(response.json()['data']['question']['codeSnippets'][0]['code'])
        return(response.json()['data']['question']['content'])

    def submit(self, filename):
        # typed_code = open(filename,'r').read()
        data = {
            'lang': 'java',
            'question_id': '2',
            'typed_code': open(filename,'r').read()
        }
        response = self.session.post(self.submit_url, data=json.dumps(data), headers=self.headers)
        print(response.json())
        return response.json()['submission_id']
    
    # def test(self):
        
    #     print(file_context)

# l = Leetcode()
# l.login('Clavier-Zhang', 'zyc990610')
# l.submit('1-two-sum.java')

