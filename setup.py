#!/usr/bin/env python

from setuptools import setup

setup(name='kyk',
      version='0.1',
      description='sass, css, js minifier watchscript',
      install_requires = ['csscompressor', 'colorama', 'jsmin', 'libsass', 'pyinotify', 'pyaml'],
      author='a-t-x',
      author_email='atx@drecks-provider.de',
      url='https://gitlab.drecks-provider.de/werkzeuge/kyk',
      download_url='https://gitlab.drecks-provider.de/werkzeuge/kyk/repository/archive.tar.gz?ref=release',
      py_modules=['kyk'],
      scripts=['kyk/kyk'],
      classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
     )