#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

DESCRIPTION = 'Simplified EVE Online SDE Access in Django'

with open('README.md') as f:
    LONG_DESCRIPTION = f.read()

from evesde import __version__ as VERSION

setup(
    name='django-evesde',
    version=VERSION,
    packages=find_packages(exclude='example_project'),
    author='Andrew Williams',
    author_email='andy@tensixtyone.com',
    url='https://github.com/nikdoof/django-evesde',
    license='BSD 3-Clause',
    include_package_data=True,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    install_requires=['Django>=1.6', 'eveapi'],
    platforms=['any'],
    classifiers=[],
)
