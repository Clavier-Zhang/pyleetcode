from setuptools import setup, find_packages

setup(
    name='pyleetcode',
    version='1.0.10',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'bs4',
        'requests',
        'colorama',
    ],
    entry_points='''
        [console_scripts]
        leet=src.commands:leet
    ''',
)