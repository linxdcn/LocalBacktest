#!/usr/bin/env python
# coding: utf8

VERSION = '0.0.1'

import sys

from setuptools import setup

extra_args = {}

setup(name='localbacktest',
      version=VERSION,
      description='localbacktest',
      author='linxdcn',
      url='https://github.com/linxdcn/LocalBacktest',
      packages=['localbacktest'],
      install_requires=['numpy>=1.14',
                        'pandas>=0.22',
                        'matplotlib>=2.1.0'],
      **extra_args)