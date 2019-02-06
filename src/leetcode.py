import requests
import json
from bs4 import BeautifulSoup

s = requests.session()

class Leetcode:

    session = None

    headers = {
        'Origin': 'https://leetcode.com',
        'Referer': 'https://leetcode.com',
        'X-Requested-With': 'XMLHttpRequest',
    }

    login_url = 'https://leetcode.com/accounts/login/'
    graphql = 'https://leetcode.com/graphql'

    def __init__(self, username, password):
        self.session = requests.session()
        self.login(username, password)

    def get_cookie(self, cookies, attribute):
        cookies = str(cookies)
        start = cookies.index(attribute)+1+len(attribute)
        cookies = cookies[start:len(cookies)]
        start = cookies.index(' ')
        return cookies[0:start]
    
    def get_first_CSRFtoken(self):
        response = s.head(self.login_url)
        return self.get_cookie(response.cookies, 'csrftoken')

    def login(self, username, password):
        CSRFtoken = self.get_first_CSRFtoken()
        self.headers['Cookie'] = 'csrftoken=' + CSRFtoken + ';'
        data = {
            'csrfmiddlewaretoken': CSRFtoken,
            'login': username,
            'password': password
        }
        s.post(self.login_url, data=data, headers=self.headers)
        sessionCSRF = self.get_cookie(s.cookies, 'csrftoken')
        sessionId = self.get_cookie(s.cookies, 'LEETCODE_SESSION')
        self.headers['Cookie'] = 'LEETCODE_SESSION=' + sessionId + ';csrftoken=' + sessionCSRF + ';'
        self.headers['X-CSRFToken'] = sessionCSRF

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
        response = s.post(self.graphql, data=data, headers=self.headers)
        
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
        response = s.post(self.graphql, data=data, headers=self.headers)
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
        response = s.post(self.graphql, data=data, headers=self.headers)
        print(response.json()['data']['question']['codeSnippets'][0]['code'])
        return(response.json()['data']['question']['content'])

# l = Leetcode('Clavier-Zhang', 'zyc990610')
# l.get_one_problem_by_title_slug('two-sum')
# html = l.get_one_problem('two-sum')

# soup = BeautifulSoup(html, features="html.parser")
# print(soup.get_text())

