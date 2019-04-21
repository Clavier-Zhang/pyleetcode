import click
from .client import client
from .config import lang_dict
from .cache import cache


@click.group()
def leet():
    pass


@click.command()
def login():
    """
    leet login,
    Login to your LeetCode account
    """
    client.login()


@click.command()
def logout():
    """
    leet logout,
    Logout
    """
    client.logout()


@click.command()
@click.argument('lang', default='java', type=click.Choice(lang_dict))
def lang(lang):
    """
    leet lang [language name]
    Set the coding language manually
    """
    client.set_coding_language(lang)


@click.command()
@click.argument('filename')
def submit(filename):
    """
    leet submit [filename],
    Submit solution to Leetcode\b
    leet submit 1-two-sum.java
    """
    client.check_login()
    client.submit(filename)


@click.command()
@click.argument('start', default=1, type=click.IntRange(0, 2000))
@click.argument('end', default=50, type=click.IntRange(0, 2000))
def show(start, end):
    """
    leet show [start] [end],
    Show questions by range
    """
    client.check_login()
    client.check_question_list()
    client.show(start, end)


@click.command()
@click.argument('question_id', default=1, type=click.IntRange(0, 2000))
def detail(question_id):
    """
    leet detail [question id],
    Show the detail of the question
    """
    client.check_login()
    client.check_question_list()
    client.detail(question_id)


@click.command()
@click.argument('question_id', default=1)
def start(question_id):
    """
    leet generate [question id],
    Generate the code template for the question
    """
    client.check_login()
    client.check_lang()
    client.check_question_list()
    client.create_template(question_id)


@click.command()
@click.argument('filename')
def test(filename):
    """
    leet test [filename], Test the code
    """
    client.check_login()
    client.test(filename)


@click.command()
def clean():
    """
    leet clean,
    Clean all cache
    """
    client.clean()


@click.command()
@click.argument('question_id', type = click.IntRange(0, 2000))
@click.argument('rank', default=0, type=click.IntRange(0, 21))
def diss(question_id, rank):
    """
    leet diss [question id],
    leet diss [question id] [rank],
    """
    client.check_login()
    if rank == 0:
        client.disscussion_list(question_id)
    else:
        client.disscussion_post(question_id, rank)


@click.command()
@click.argument('list_name', type=click.Choice(cache.get_company_slugs()))
@click.argument('start', type=click.IntRange(1, 1000))
@click.argument('end', type=click.IntRange(1, 1000))
def create(list_name, start, end):
    """
    leet create google 1 50
    """
    if (start > end):
        print('invalid input')
    client.check_login()
    client.create_company_list(list_name, start, end)


@click.command()
def contribute():
    client.check_login()
    client.contribute()


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


leet.add_command(create)
leet.add_command(contribute)
