#!/usr/bin/env python

from setuptools import setup

setup(name='Kyk',
      version='1.0',
      description='SASS, css, js minifier watchscript',
      install_requires = ['csscompressor', 'colorama', 'jsmin', 'libsass', 'pyinotify', 'pyaml'],
      author='Alexander Trautsch',
      author_email='at@fma-medien.de',
      url='https://gitlab.drecks-provider.de/werkzeuge/kyk',
      py_modules=['kyk.py'],
      scripts=['kyk.py']
     )