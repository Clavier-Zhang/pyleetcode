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
    pass

@click.command()
@click.argument('filename')
def submit(filename):
    """leet submit 1-two-sum.java"""
    print("submit")
    l = Leetcode()
    l.login('Clavier-Zhang', 'zyc990610')
    l.submit(filename)



leet.add_command(submit)
leet.add_command(login)


if __name__ == '__main__':
    leet()