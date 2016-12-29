#!/usr/bin/env python

from setuptools import setup

setup(
    name = 'shodan',
    version = '1.6.3',
    description = 'Python library and command-line utility for Shodan (https://developer.shodan.io)',
    author = 'John Matherly',
    author_email = 'jmath@shodan.io',
    url = 'http://github.com/achillean/shodan-python/tree/master',
    packages = ['shodan', 'shodan.cli', 'shodan.cli.converter'],
    scripts = ['bin/shodan'],
    install_requires=["simplejson", "requests>=2.2.1", "click", "click-plugins", "colorama"],
    classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
