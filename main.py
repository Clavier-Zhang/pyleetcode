import requests

login_url = 'https://leetcode.com/accounts/login/'
graphql = 'https://leetcode.com/graphql'

s = requests.session()

class leetcode:

    session = ''
    sessionCSRF = ''
    sessionId = ''

    def __init__(self):
        self.session = requests.session()

    def get_cookie(self, cookies, attribute):
        cookies = str(cookies)
        start = cookies.index(attribute)+1+len(attribute)
        cookies = cookies[start:len(cookies)]
        start = cookies.index(' ')
        return cookies[0:start]
    
    def get_CSRFtoken(self):
        response = requests.head(login_url)
        return self.get_cookie(response.cookies, 'csrftoken')

    def login(self):
        CSRFtoken = self.get_CSRFtoken()
        headers = {
            'Origin': 'https://leetcode.com',
            'Referer': 'https://leetcode.com/accounts/login/',
            'Cookie':  'csrftoken=' + CSRFtoken + ';'
        }
        data = {
            'csrfmiddlewaretoken': CSRFtoken,
            'login': 'Clavier-Zhang',
            'password': 'zyc990610'
        }
        response = s.post(login_url, data=data, headers=headers)
        cookies = s.cookies
        self.sessionCSRF = self.get_cookie(cookies, 'csrftoken')
        self.sessionId = self.get_cookie(cookies, 'LEETCODE_SESSION')

    def get_user_info(self):
        self.login()
        headers = {
            'Origin': 'https://leetcode.com',
            'Referer': 'https://leetcode.com',
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie':  'LEETCODE_SESSION=' + self.sessionId + ';csrftoken=' + self.sessionCSRF + ';',
            'X-CSRFToken': self.sessionCSRF
        }
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
        response = s.post(graphql, data=data, headers=headers, cookies=s.cookies)
        print(response.text)

l = leetcode()
l.get_user_info()