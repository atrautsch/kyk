#!/usr/bin/env python

import sys

from setuptools import setup, find_packages

if not sys.version_info[0] == 3:
    print('only python3 supported!')
    sys.exit(1)

setup(name='kyk',
      version='1.4.7',
      description='sass, css, js minifier watchscript',
      install_requires=['csscompressor', 'colorama', 'jsmin', 'libsass', 'pyinotify', 'pyaml'],
      author='atrautsch',
      author_email='atrautsch@cs.uni-goettingen.de',
      url='https://github.com/atrautsch/kyk',
      packages=find_packages(),
      scripts=['kyk/kyk'],
      keywords='minifier watchscript',
      classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
)
