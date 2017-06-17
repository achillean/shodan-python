#!/usr/bin/env python

from setuptools import setup

dependencies = open('requirements.txt', 'r').read().split('\n')

setup(
    name = 'shodan',
    version = '1.6.12',
    description = 'Python library and command-line utility for Shodan (https://developer.shodan.io)',
    author = 'John Matherly',
    author_email = 'jmath@shodan.io',
    url = 'http://github.com/achillean/shodan-python/tree/master',
    packages = ['shodan', 'shodan.cli', 'shodan.cli.converter'],
    scripts = ['bin/shodan'],
    install_requires = dependencies,
    classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
