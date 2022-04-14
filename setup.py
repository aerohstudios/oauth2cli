#!/usr/bin/env python

from re import M
from setuptools import setup, find_packages

version = '1.0.0'

setup(
    name='oauthcli',
    version=version,
    description='Generic OAuth 2.0 command-line utility to retrieve access tokens. Uses Python standard library!',
    author='Shiv Deepak Muddada',
    author_email='shiv@aeroh.org',
    url='https://github.com/aerohstudios/oauthcli',
    license='Apache Software License (http://www.apache.org/licenses/LICENSE-2.0)',
    packages=find_packages(),
    platforms='any',
    python_requires='>=3.0',
    entry_points={
        'console_scripts': [
            'oauthcli = oauthcli:main'
        ]},
    long_description=open('README.md').read(),
    install_requires=[],
    classifiers=[
        # Supported classifiers: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Internet :: WWW/HTTP :: Session',
        'Topic :: Software Development'
    ]
)
