#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name: setup.py

from setuptools import setup


setup(
    name='claim_rdf',
    version='0.0.1',
    url='https://github.com/AtomsForPeace/claim_rdf',
    license='BSD',
    author='Adam Bannister',
    author_email='adam.p.bannister@posteo.net',
    description='A simple async library for handling claims in an RDF store',
    long_description=__doc__,
    install_requires=['aiosparql', ],
)
