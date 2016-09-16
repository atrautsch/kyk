#!/usr/bin/env python

import sys

from setuptools import setup, find_packages

if not sys.version_info[0] == 3:
    print('only python3 supported!')
    sys.exit(1)

setup(name='kyk',
      version='1.4.4',
      description='sass, css, js minifier watchscript',
      install_requires = ['csscompressor', 'colorama', 'jsmin', 'libsass', 'pyinotify', 'pyaml'],
      author='a-t-x',
      author_email='atx@drecks-provider.de',
      url='https://gitlab.drecks-provider.de/werkzeuge/kyk',
      download_url='https://gitlab.drecks-provider.de/werkzeuge/kyk/repository/archive.tar.gz?ref=release',
      packages=find_packages(),
      #py_modules=['kyk.py'],
      scripts=['kyk/kyk'],
      keywords='minifier watchscript',
      classifiers = [
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
     )
