import click
from .leetcode import Leetcode
from .client import Client

client = Client()

@click.group()
def leet():
    try:  
        client.check_login()
    except Exception as e:
        print(e)
        quit()
    

@click.command()
def login():
    print('login')

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