import click
from src import leetcode

@click.group()
def leet():
    pass

@click.command()
def get():
    print("23333333")

@click.command()
def test1():
    """Example script."""
    click.echo('Hello World!')

leet.add_command(get)
leet.add_command(test1)

if __name__ == '__main__':
    leet()