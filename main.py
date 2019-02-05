import requests

login_url = 'https://leetcode.com/accounts/login/'
graphql = 'https://leetcode.com/graphql'

s = requests.session()

class leetcode:

    session = ''

    def __init__(self):
        self.session = requests.session()
    
    def get_CSRFtoken(self):
        response = requests.head(login_url)
        cookies = response.headers['Set-Cookie']
        start = cookies.index('csrf')+10
        cookies = cookies[start:len(cookies)]
        start = cookies.index(';')
        return cookies[0:start]

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
        # cookies = response.headers['Set-Cookie']
        # start = cookies.index('csrf')+10
        # cookies = cookies[start:len(cookies)]
        # start = cookies.index(';')
        print(s.cookies)
        # return cookies[0:start]


    def get_user_info(self):
        CSRFtoken = self.login()
        headers = {
            'Origin': 'https://leetcode.com',
            'Referer': 'https://leetcode.com',
            'Cookie':  'csrftoken=' + CSRFtoken + ';'
        }
        data = {
            'csrfmiddlewaretoken': CSRFtoken,
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
        response = s.post(graphql, data=data, headers=headers)
        print(response.text)

l = leetcode()
l.login()
