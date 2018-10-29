#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()


setup(
    name='nameko-structlog',
    version='0.1.0',
    description='Nameko extension exposing a structlog dependency injector',
    long_description=readme + '\n\n' + history,
    author='Spyros Markopoulos',
    author_email='mail.doctor46@gmail.com',
    url='https://github.com/tyler46/nameko-structlog',
    include_package_data=True,
    packages=find_packages(include=['nameko_structlog']),
    install_requires=[
        "nameko>=2.5.0",
        "structlog>=18.2.0",
    ],
    extras_require={
        'dev': [
            'coverage==4.5.1',
            'pip==18.1',
            'bumpversion==0.5.3',
            'flake8==3.5.0',
            'pylint>=1.9.3',
            'twine>=1.12.1',
            'wheel>=0.32.2',
        ],
        'colors': ['colorama>=0.4.0'],
    },
    test_suite='tests',
    tests_require=[
        'pytest'
    ],
    zip_safe=False,
    license='Apache License, Version 2.0',
    keywords='nameko logging structlog',
    classifiers=[
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet',
    ],
)
