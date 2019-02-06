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
    submit_url = 'https://leetcode.com/problems/add-two-numbers/submit/'

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
        self.session.post(self.login_url, data=data, headers=self.headers)
        sessionCSRF = self.get_cookie(self.session.cookies, 'csrftoken')
        sessionId = self.get_cookie(self.session.cookies, 'LEETCODE_SESSION')
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
        response = self.session.post(self.graphql, data=data, headers=self.headers)
        
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
        response = self.session.post(self.graphql, data=data, headers=self.headers)
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
        response = self.session.post(self.graphql, data=data, headers=self.headers)
        print(response.json()['data']['question']['codeSnippets'][0]['code'])
        return(response.json()['data']['question']['content'])

    def submit(self):
        data = {
            'lang': 'java',
            'question_id': '2',
            'typed_code': '''
                /**
                * Definition for singly-linked list.
                * public class ListNode {
                *     int val;
                *     ListNode next;
                *     ListNode(int x) { val = x; }
                * }
                */
                class Solution {
                    public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
                        ListNode dummy = new ListNode(0);
                        ListNode head = dummy;
                        int carry = 0;
                        while (l1 != null || l2 != null || carry != 0) {
                            int sum = carry + (l1 == null ? 0 : l1.val) + (l2 == null ? 0 : l2.val);
                            carry = sum/10;
                            head.next = new ListNode(sum%10);
                            head = head.next;
                            l1 = (l1 == null ? l1 : l1.next);
                            l2 = (l2 == null ? l2 : l2.next);
                        }
                        return dummy.next;
                    }
                }
            '''
        }
        response = self.session.post(self.submit_url, data=json.dumps(data), headers=self.headers)
        print(response.text)
    
    def test(self):
        return

l = Leetcode('Clavier-Zhang', 'zyc990610')
l.submit()




