#!/usr/bin/env python

from setuptools import setup, find_packages
import sys

python_version = sys.version_info

install_deps = []
with open('requirements.txt') as file_requirements:
    install_deps = file_requirements.read().splitlines()

version = ''
with open('VERSION') as f:
    version = f.readline().strip()

setup(name='gitstats',
      version=version,
      description='Python package for counting download statistics for Git repositories',
      author='Devarshi Ghoshal',
      author_email='dghoshal@lbl.gov',
      keywords='',
      packages=find_packages(exclude=['ez_setup']),
      include_package_data=True,
      zip_safe=False,
      classifiers=['Development Status :: 1 - Alpha',
                   'Intended Audience :: Developers/Admins',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2.7',
                   'Topic :: Engineering',
                   'License :: OSI Approved :: BSD License'
      ],
      install_requires=install_deps,
      entry_points={'console_scripts': ['gitstats = gitstats:main']},
      data_files=[('', ['VERSION'])]
)
