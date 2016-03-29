#!/usr/bin/env python

from setuptools import setup

setup(
        name='dechat',
        version='0.1.0',
        description='Distributed, encrypted chat client',
        author='L.J. Hill',
        author_email='foehawk@gmail.com',
        url='https://github.com/robobrobro/dechat',
        packages=['dechat'],
        install_requires=[
            'cryptography',
        ],
)
