
from .local import Local
from .leetcode import Leetcode
import click

class Client:

    local = Local()

    leetcode = Leetcode()

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
            return
        problem_slug = problem_summary['stat']['question__article__slug']
        # if the detail is not in the cache, fetch from leetcode
        if not self.local.check_problem_details_status(question_id):
            print('detail not in the cache, fetch from leetcode')
            self.leetcode.get_one_problem_by_title_slug(problem_slug)

        question_detail = self.local.fetch_one_problem_detail(question_id)
        print(question_detail)
    
    def start(self, question_id):
        return