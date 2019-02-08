
from .cache import Cache
from .leetcode import Leetcode
from .system import System
from .config import lang_dict
from .screen import Screen
import click

class Client:

    cache = Cache()

    leetcode = Leetcode()

    system = System()

    screen = Screen()

    # login methods
    def check_login(self):
        if (not self.cache.check_user_account_statue()):
            self.login()
        if (not self.cache.check_user_token_statue()):
            if not self.update_token():
                self.login()

    def login(self):
        while True:
            username = click.prompt('Please enter your username')
            password = click.prompt('Please enter your password', hide_input=True)
            self.cache.save_username_and_password(username, password)
            if self.leetcode.login(username, password):
                self.screen.print_login_success_message()
                break
            else:
                self.screen.print_login_fail_message()

    def logout(self):
        self.cache.clear_user()
        self.screen.print_logout_success_message()
        
    def update_token(self):
        username = self.cache.get_user_username()
        password = self.cache.get_user_password()
        return self.leetcode.login(username, password)

    def lang(self, lang):
        self.cache.save_user_lang(lang)
        self.screen.print_update_lang_message(lang)


    # question methods
    def submit(self, filename):
        self.leetcode.submit(filename)

    def show(self, start, end):
        if not self.cache.check_question_index_status():
            self.leetcode.get_all_problems()
        self.screen.print_question_summarys(self.cache.get_question_summarys_by_range(start, end))
        

    def detail(self, question_id):
        # check the index of problems
        if not self.cache.check_question_index_status():
            self.leetcode.get_all_problems()
        # use the problem index to convert question_id to title_slug
        problem_summary = self.cache.get_question_summary_by_question_id(question_id)
        if (problem_summary == None):
            print("the problem does not exist")
            return None
        problem_slug = problem_summary['stat']['question__title_slug']
        # if the detail is not in the cache, fetch from leetcode
        if not self.cache.check_question_detail_status_by_question_id(question_id):
            print('detail not in the cache, fetch from leetcode')
            self.leetcode.get_one_problem_by_title_slug(problem_slug)

        question_detail = self.cache.get_question_detail_by_question_id(question_id)
        self.screen.print_question_detail(question_detail)
        return question_detail
    
    def start(self, question_id):
        # check user's language
        if not self.cache.check_user_lang_status():
            lang = click.prompt('Please enter your preferred language')
            if lang not in lang_dict:
                print('does not support this language')
                return
            self.cache.save_user_lang(lang)
        lang = self.cache.get_user_lang()
        # check the index of problems
        if not self.cache.check_question_index_status():
            self.leetcode.get_all_problems()
        # use the problem index to convert question_id to title_slug
        problem_summary = self.cache.get_question_summary_by_question_id(question_id)
        if (problem_summary == None):
            print("the problem does not exist")
            return None
        problem_slug = problem_summary['stat']['question__article__slug']

        # if the detail is not in the cache, fetch from leetcode
        if not self.cache.check_question_detail_status_by_question_id(question_id):
            print('detail not in the cache, fetch from leetcode')
            self.leetcode.get_one_problem_by_title_slug(problem_slug)

        question_detail = self.cache.get_question_detail_by_question_id(question_id)
        if question_detail == None:
            return
        code_templates = question_detail['codeSnippets']
        sample_test_case = question_detail['sampleTestCase']
        for code_template in code_templates:
            if code_template['langSlug'] == lang:
                self.system.generate_code_file(str(question_id)+'-'+problem_slug, lang, code_template['code'], sample_test_case)

    def test(self, filename):
        self.leetcode.test(filename)