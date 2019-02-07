import click
from .leetcode import Leetcode
from .client import Client

client = Client()

@click.group()
def leet():
    result = True
    try:  
        client.check_login()
    except Exception as e:
        print(e)
        quit()
    if (not result):
        quit()

@click.command()
def login():
    pass

@click.command()
@click.argument('filename')
def submit(filename):
    """leet submit 1-two-sum.java"""
    client.submit(filename)

@click.command()
@click.argument('start', default=1)
@click.argument('end', default=50)
def show(start, end):
    """leet show 1 50"""
    print("show")

    print(start)
    print(end)
    client.show(start, end)

@click.command()
@click.argument('question_id', default=1)
def detail(question_id):
    """leet show 1 50"""
    print("detail")
    print(question_id)

@click.command()
@click.argument('question_id', default=1)
def start(question_id):
    """leet show 1 50"""
    print("start")
    print(question_id)

leet.add_command(submit)
leet.add_command(login)
leet.add_command(show)
leet.add_command(detail)
leet.add_command(start)

if __name__ == '__main__':
    leet()