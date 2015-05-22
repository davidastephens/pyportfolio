#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ast import parse
import os
from setuptools import setup


NAME = 'pyportfolio'


def version():
    """Return version string."""
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                           'pyportfolio',
                           '__init__.py')) as input_file:
        for line in input_file:
            if line.startswith('__version__'):
                return parse(line).body[0].value.s


def readme():
    with open('README.rst') as f:
        return f.read()

INSTALL_REQUIRES = (
    ['pandas']
)

setup(
    name=NAME,
    version=version(),
    description="Library for managing porfolios of stocks and options",
    long_description=readme(),
    license='BSD License',
    author='David Stephens',
    author_email='dstephens99@gmail.com',
    url='https://github.com/dstephens99/pyportfolio',
    classifiers=[
        'Development Status :: 5 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Cython',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering',
    ],
    keywords='data',
    install_requires=INSTALL_REQUIRES,
    packages=['pyportfolio'],
    test_suite='tests',
    zip_safe=False,
)
