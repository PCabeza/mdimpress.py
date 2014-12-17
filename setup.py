#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement
import sys
import os
import getpass
import codecs
from setuptools import setup
from setuptools.command.install import install

setup(
    name='mdimpress.py',
    version="0.1",
    license='GPL',
    author='Pablo Cabeza',
    author_email='lemniscata.lmn@gmail.com',
    description='mdimpress.py is a command and framework for building '
                'presentations from markdown based on impess.js',
    packages=['mdimpress'],
    package_data ={'mdimpress': ['data/grunt/*','data/template/*']},


    entry_points={
        'console_scripts': [
            'mdimpress = mdimpress:main',
        ]
    },
)