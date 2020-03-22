#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

with open('pytest_timer/__init__.py') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

setup(
    name='pytest-timer',
    version=version,
    description='A timer plugin for pytest',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=', '.join([
        'Stanislav Kudriashev',
    ]),
    url='https://https://github.com/skudriashev/pytest-timer',
    packages=['pytest_timer'],
    install_requires=[
        'pytest',
    ],
    license='MIT',
    entry_points={"pytest11": ["name_of_plugin = pytest_timer.plugin"]},
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Testing',
        'Environment :: Console',
        'Framework :: Pytest',
    ],
)
