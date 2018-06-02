#!/usr/bin/env python

from setuptools import setup

dependencies = open('requirements.txt', 'r').read().split('\n')

setup(
    name = 'shodan',
    version = '1.8.1',
    description = 'Python library and command-line utility for Shodan (https://developer.shodan.io)',
    author = 'John Matherly',
    author_email = 'jmath@shodan.io',
    url = 'http://github.com/achillean/shodan-python/tree/master',
    packages = ['shodan', 'shodan.cli', 'shodan.cli.converter'],
    entry_points = {'console_scripts': ['shodan = shodan.__main__:main']},
    install_requires = dependencies,
    keywords = ['security', 'network'],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
