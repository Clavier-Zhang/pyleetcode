from setuptools import setup, find_packages

setup(
    name='pyleetcode',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'bs4',
        'requests',
    ],
    entry_points='''
        [console_scripts]
        leet=src.commands:leet
        submit=src.commands:submit
        test1=src.commands:test1
    ''',
)