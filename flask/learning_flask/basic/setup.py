#!/usr/bin/env python
# encoding: utf-8

import os
from setuptools import setup

setup(
        name = 'basic',
        version ='1.0',
        license='GNU',
        author ="simonpatrick",
        description="flask basic",
        packages = ['basic'],
        platforms ='any',
        install_requires=[
            "flask"
            ],
        classifiers = [
            'Development status:: 4 -Beta',
            'Topic :: Internet :: WWW/HTTP:: Dynamic Content'
            ]
        )
