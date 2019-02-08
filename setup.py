from setuptools import setup, find_packages

setup(
    name='pyleetcode',
    version='0.2',
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
        submit=src.commands:submit
        login=src.commands:login
        show=src.commands:show
        detail=src.commands:detail
        start=src.commands:start
        lang=src.commands:lang
    ''',
)