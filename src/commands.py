import click
from .leetcode import Leetcode

@click.group()
def leet():
    pass

@click.command()
@click.argument('filename')
def submit(filename):
    print("submit")
    l = Leetcode('Clavier-Zhang', 'zyc990610')
    l.submit(filename)

@click.command()
def test1():
    """Example script."""
    click.echo('Hello World!')

leet.add_command(submit)
leet.add_command(test1)

if __name__ == '__main__':
    leet()