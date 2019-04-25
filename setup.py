from setuptools import setup, find_packages

setup(
    name='pyleetcode',
    version='3.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'bs4',
        'requests',
        'colorama',
        'pathlib',
        'pytest',
    ],
    entry_points='''
        [console_scripts]
        leet=src.commands:leet
    ''',
)