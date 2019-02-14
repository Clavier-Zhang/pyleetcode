import click
from .leetcode import Leetcode
from .client import Client
from .config import lang_dict

client = Client()

@click.group()
def leet():
    pass

@click.command()
def login():
    """Login to your Leetcode account"""
    client.login()

@click.command()
def logout():
    """Logout to your Leetcode account"""
    client.logout()

@click.command()
@click.argument('lang', default='java', type=click.Choice(lang_dict))
def lang(lang):
    """Set the coding language manually\b
       leet lang java"""
    client.lang(lang)

@click.command()
@click.argument('filename')
def submit(filename):
    """
    Submit solution to Leetcode\b
    leet submit 1-two-sum.java
    """
    client.check_login()
    client.submit(filename)

@click.command()
@click.argument('start', default=1, type=click.IntRange(0, 2000))
@click.argument('end', default=50, type=click.IntRange(0, 2000))
def show(start, end):
    """Show questions by range"""
    client.check_login()
    client.show(start, end)

@click.command()
@click.argument('question_id', default=1, type=click.IntRange(0, 2000))
def detail(question_id):
    """Show the detail of the question"""
    client.check_login()
    client.detail(question_id)

@click.command()
@click.argument('question_id', default=1)
def start(question_id):
    """Generate the code template for the question"""
    client.check_login()
    client.start(question_id)


@click.command()
@click.argument('filename')
def test(filename):
    """Test the code"""
    client.check_login()
    client.test(filename)


@click.command()
def clean():
    """Clean all cache"""
    client.clean()


@click.command()
@click.argument('question_id', type = click.IntRange(0, 2000))
@click.argument('rank', default=0, type=click.IntRange(0, 21))
def diss(question_id, rank):
    client.check_login()
    if rank == 0:
        client.disscussion_list(question_id)
    else:
        client.disscussion_post(question_id, rank)


leet.add_command(login)
leet.add_command(logout)
leet.add_command(lang)
leet.add_command(clean)

leet.add_command(show)
leet.add_command(detail)
leet.add_command(start)

leet.add_command(test)
leet.add_command(submit)
leet.add_command(diss)

