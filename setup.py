#!/usr/bin/env python

from distutils.core import setup

from shodan import __version__ as version

setup(
    name = 'shodan',
    version = version,
    description = 'Python library for SHODAN (http://www.shodanhq.com)',
    author = 'John Matherly',
    author_email = 'jmath@shodanhq.com',
    url = 'http://github.com/achillean/shodan-python/tree/master',
    packages = ['shodan'],
    classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
