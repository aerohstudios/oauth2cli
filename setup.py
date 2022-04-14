#!/usr/bin/env python

from setuptools import setup, find_packages

version = open('oauth2cli/VERSION').read().strip()

setup(
    name='oauth2cli',
    version=version,
    description='Generic OAuth 2.0 command-line utility to retrieve access tokens. Uses Python standard library!',
    author='Shiv Deepak Muddada',
    author_email='shiv@aeroh.org',
    url='https://github.com/aerohstudios/oauth2cli',
    license='Apache Software License (http://www.apache.org/licenses/LICENSE-2.0)',
    packages=find_packages(),
    platforms='any',
    python_requires='>=3.0',
    entry_points={
        'console_scripts': [
            'oauth2cli = oauth2cli:main'
        ]},
    long_description=open('README.rst').read(),
    install_requires=[],
    package_data={'oauth2cli': ['VERSION']},
    include_package_data=True,
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
