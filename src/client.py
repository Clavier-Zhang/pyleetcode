
from .local import Local
from .leetcode import Leetcode
import click

class Client:

    local = Local()
    leetcode = Leetcode()

    def check_login(self):
        self.local.fetch_login_status()
        self.login()

    def login(self):
        username = click.prompt('Please enter your username')
        password = click.prompt('Please enter your password', hide_input=True)
        self.local.save_username_and_password(username, password)

    def test(self):
        print('2333')