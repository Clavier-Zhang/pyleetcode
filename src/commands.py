import click
from .leetcode import Leetcode
from .client import Client

client = Client()

@click.group()
def leet():
    client.check_login()
    return

@click.command()
def login():
    return

@click.command()
@click.argument('filename')
def submit(filename):
    """Example script."""
    print("submit")
    l = Leetcode()
    l.login('Clavier-Zhang', 'zyc990610')
    l.submit(filename)



leet.add_command(submit)
leet.add_command(login)


if __name__ == '__main__':
    leet()