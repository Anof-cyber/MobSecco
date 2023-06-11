#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
from setuptools import setup, find_packages
from os import path
this_directory = path.abspath(path.dirname(__file__))
with io.open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    desc = f.read()

setup(
    name='mobsecco',
    version=__import__('MobSecco').__version__,
    description='Clone Cordova application for fun and bypassing security restrictions for pentesting',
    long_description=desc,
    long_description_content_type='text/markdown',
    author='Sourav Kalal',
    author_email='kalalsourav20@gmail.com',
    license='MIT license',
    url='https://github.com/Anof-cyber/MobSecco',
    zip_safe=False,
    install_requires=[
        'pyaxmlparser==0.3.28'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Operating System :: OS Independent',
        'Topic :: Security',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'mobsecco = mobsecco:main'
        ]
    },
    keywords=['mobsecco', 'bug bounty', 'android', 'pentesting', 'security'],
)