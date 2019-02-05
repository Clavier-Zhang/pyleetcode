import requests


s = requests.session()

class leetcode:

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
        print(response.text)

l = leetcode('Clavier-Zhang', 'zyc990610')
l.get_user_info()