import click
from .leetcode import Leetcode
from .client import Client
from .config import lang_dict

client = Client()

@click.group()
def leet():
    client.check_login()


@click.command()
def login():
    pass

@click.command()
def logout():
    client.logout()

@click.command()
@click.argument('lang', default='java', type=click.Choice(lang_dict))
def lang(lang):
    """leet lang java"""
    client.lang(lang)



@click.command()
@click.argument('filename')
def submit(filename):
    """leet submit 1-two-sum.java"""
    client.submit(filename)

@click.command()
@click.argument('start', default=1, type=click.IntRange(0, 2000))
@click.argument('end', default=50, type=click.IntRange(0, 2000))
def show(start, end):
    """leet show 1 50"""
    client.show(start, end)

@click.command()
@click.argument('question_id', default=1, type=click.IntRange(0, 2000))
def detail(question_id):
    """leet detail 1"""
    client.detail(question_id)

@click.command()
@click.argument('question_id', default=1)
def start(question_id):
    """leet start 1 50"""
    client.start(question_id)


@click.command()
@click.argument('filename')
def test(filename):
    """leet test 1-two-sum.java"""
    client.test(filename)


leet.add_command(login)
leet.add_command(logout)
leet.add_command(lang)

leet.add_command(show)
leet.add_command(detail)
leet.add_command(start)

leet.add_command(test)
leet.add_command(submit)

