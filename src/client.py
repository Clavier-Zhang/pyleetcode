
from .local import Local
from .leetcode import Leetcode
from .system import System

import click

class Client:

    local = Local()

    leetcode = Leetcode()

    system = System()

    langs = ['cpp', 'java', 'python', 'python3', 'c', 'csharp', 'javascript', 'ruby', 'swift', 'golang', 'scala', 'kotlin', 'rust', 'php']

    def check_login(self):
        if (not self.local.fetch_account_status()):
            self.login()
        if (not self.local.fetch_token_status()):
            self.update_token()

    def login(self):
        click.echo('You need to login first')
        username = click.prompt('Please enter your username')
        password = click.prompt('Please enter your password', hide_input=True)
        self.local.save_username_and_password(username, password)
        self.update_token()
        print('Login success')

    def update_token(self):
        user = self.local.fetch_user()
        self.leetcode.login(user['username'], user['password'])

    def submit(self, filename):
        self.leetcode.submit(filename)

    def show(self, start, end):
        if not self.local.check_problems_status():
            self.leetcode.get_all_problems()
        print(self.local.fetch_problems_with_range(start, end))
        

    def detail(self, question_id):
        # check the index of problems
        if not self.local.check_problems_status():
            self.leetcode.get_all_problems()
        # use the problem index to convert question_id to title_slug
        problem_summary = self.local.fetch_problem_by_id(question_id)
        if (problem_summary == None):
            print("the problem does not exist")
            return None
        problem_slug = problem_summary['stat']['question__article__slug']
        # if the detail is not in the cache, fetch from leetcode
        if not self.local.check_problem_details_status(question_id):
            print('detail not in the cache, fetch from leetcode')
            self.leetcode.get_one_problem_by_title_slug(problem_slug)

        question_detail = self.local.fetch_one_problem_detail(question_id)
        print(question_detail)
        return question_detail
    
    def start(self, question_id):
        # check user's language
        if not self.local.check_user_lang_status():
            lang = click.prompt('Please enter your preferred language')
            if lang not in self.langs:
                print('does not support this language')
                return
            self.local.save_user_lang(lang)
        lang = self.local.fetch_user_lang()
        # check the index of problems
        if not self.local.check_problems_status():
            self.leetcode.get_all_problems()
        # use the problem index to convert question_id to title_slug
        problem_summary = self.local.fetch_problem_by_id(question_id)
        if (problem_summary == None):
            print("the problem does not exist")
            return None
        problem_slug = problem_summary['stat']['question__article__slug']

        # if the detail is not in the cache, fetch from leetcode
        if not self.local.check_problem_details_status(question_id):
            print('detail not in the cache, fetch from leetcode')
            self.leetcode.get_one_problem_by_title_slug(problem_slug)
        question_detail = self.local.fetch_one_problem_detail(question_id)
        if question_detail == None:
            return

        
        code_templates = question_detail['codeSnippets']
        for code_template in code_templates:
            if code_template['langSlug'] == lang:
                self.system.generate_code_file(str(question_id)+'-'+problem_slug, lang, code_template['code'])

    def lang(self, lang):
        self.local.save_user_lang(lang)

    def test(self, filename):
        self.leetcode.test(filename)