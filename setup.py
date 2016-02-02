#!/usr/bin/env python

#from setuptools import setup
from setuptools import setup, find_packages

setup(name='kyk',
      version='1.0',
      description='sass, css, js minifier watchscript',
      install_requires = ['csscompressor', 'colorama', 'jsmin', 'libsass', 'pyinotify', 'pyaml'],
      author='a-t-x',
      author_email='atx@drecks-provider.de',
      url='https://gitlab.drecks-provider.de/werkzeuge/kyk',
      download_url='https://gitlab.drecks-provider.de/werkzeuge/kyk/repository/archive.tar.gz?ref=release',
      packages=find_packages(),
      #py_modules=['kyk.py'],
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
