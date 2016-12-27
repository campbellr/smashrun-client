#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

# workaround for python issue #15881
try:
    import multiprocessing
except ImportError:
    pass


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'requests',
    'requests-oauthlib'
]

test_requirements = ['unittest2']

setup(
    name='smashrun-client',
    version='0.5.0',
    description="A Python client for the Smashrun API",
    long_description=readme + '\n\n' + history,
    author="Ryan Campbell",
    author_email='campbellr@gmail.com',
    url='https://github.com/campbellr/smashrun-client',
    packages=[
        'smashrun',
    ],
    package_dir={'smashrun':
                 'smashrun'},
    include_package_data=True,
    install_requires=requirements,
    license="Apache",
    zip_safe=False,
    keywords='smashrun',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='unittest2.collector',
    tests_require=test_requirements
)
