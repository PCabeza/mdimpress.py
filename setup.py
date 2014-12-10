#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement
import sys
import os
import getpass
import codecs
from setuptools import setup
from setuptools.command.install import install

# import glob,os

# GRUNTFILES = filter(os.path.isfile,glob.glob('./grunt/*'))
# TEMPLATEFILES = filter(os.path.isfile,glob.glob('./template/*'))

setup(
    name='mdimpress.py',
    version="0.1",
    license='GPL',
    author='Pablo Cabeza',
    author_email='josepablocg@gmail.com',
    description='mdimpress.py is a command and framework for building '
                'presentations from markdown based on impess.js',
    #long_description=read("README.md"),
    #url='http://www.geeknote.me',
    packages=['mdimpress'],
    package_data ={'mdimpress': ['data/grunt/*','data/template/*']},


    # classifiers=[
    #     'Development Status :: 3 - Alpha',
    #     'Intended Audience :: End Users/Desktop',
    #     'License :: OSI Approved :: GNU General Public License (GPL)',
    #     'Environment :: Console',
    #     'Natural Language :: English',
    #     'Operating System :: OS Independent',
    #     'Programming Language :: Python',
    #     'Topic :: Utilities',
    # ],

    install_requires=[
        #'distutils'
    ],

    entry_points={
        'console_scripts': [
            'mdimpress = mdimpress:main',
        ]
    },
#    cmdclass={
#        'install': full_install
#    },
    # platforms='Any',
    # test_suite='tests',
    # zip_safe=False,
    # keywords='Evernote, console'
)