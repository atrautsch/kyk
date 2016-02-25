#!/usr/bin/env python3

import os
import time

import yaml
import sass
import pyinotify

from colorama import init, Fore, Style
from jsmin import jsmin
from csscompressor import compress

VERSION = 1.1

class Kyk(object):
    """Kyk

    Build JS
    - if min: minify in place, append _minifed
    - concat to destfile

    Build SASS:
    - compile SASS file
    - concat to destfile

    Build partial js not yet implemented completely
    """
    
    def __init__(self, folder, debug):
        self._folder = folder
        self._debug = debug

        cfgfile = os.path.normpath(os.path.join(self._folder, 'kyk.yaml'))
        if not os.path.isfile(cfgfile):
            raise Exception('no config file "{}" found!'.format(cfgfile))

        with open(cfgfile, 'r', encoding='utf-8') as f:
            dat = f.read()

        self._cfg = yaml.load(dat)

        self._js = {}
        self._css = {}
        self._jswatchlist = []
        self._listen_events = []
        self._timestamp_file = None

        init()
        self._load_config()


    def _load_config(self):
        self._version = self._cfg['version']
        self._listen_events = self._cfg['events']
        if 'timestamp_file' in self._cfg.keys():
            self._timestamp_file = self._cfg['timestamp_file']

        for minfile in self._cfg.keys():
            if minfile.endswith('.js'):
                jsfile = self._cfg[minfile]
                minify = False
                
                for jsfile in self._cfg[minfile]:
                    if jsfile.startswith('min:'):
                        minify = True
                        jsfile = jsfile.split('min:')[1].strip()
                    if minfile not in self._js.keys():
                        self._js[minfile] = []

                    self._js[minfile].append({'file': os.path.abspath(jsfile), 'minify': minify})
                    self._jswatchlist.append(os.path.abspath(jsfile))
            elif minfile.endswith('.css'):
                self._css[minfile] = self._cfg[minfile]

        print('listening on:')
        print(self._listen_events)
        print('config version: {}'.format(self._version))
        print('Kyk version: {}'.format(VERSION))

    def watch_forever(self):
        # first run, build everything
        self.build_js()
        self.build_sass()

        # now only changed files
        wm = pyinotify.WatchManager()
        notifier = pyinotify.Notifier(wm, default_proc_fun=self.handler)
        wm.add_watch(self._folder, pyinotify.ALL_EVENTS, rec=True, auto_add=True)
        notifier.loop()

    def handler(self, event):
        # catch every scss file change, we can do this here because we are limited by the watchpath
        if getattr(event, 'pathname'):
            if event.pathname.endswith('.scss'):
                if event.maskname in self._listen_events:
                    print('{} changed!'.format(event.pathname))
                    self.build_sass()

            # catch only changes to our configured jsfiles
            elif event.pathname in self._jswatchlist:
                if event.maskname in self._listen_events:
                    print('{} changed!'.format(event.pathname))
                    self.build_js()

    def build_js(self):
        """minify everything, then concat everything
        """
        print('building js...')
        for minfile in self._js.keys():
            with open(minfile, 'w', encoding='utf-8') as f:
                for jsfile in self._js[minfile]:
                    if jsfile['minify'] and not self._debug:
                        self.minify_js(jsfile['file'])

                    out = self._load_js(jsfile['file'])

                    f.write(out)
        print('finished')
        self._update_timestamp()

    def concat_js(self, destfile):
        print('building {}...'.format(destfile))
        with open(destfile, 'w', encoding='utf-8') as f:
            for jsfile in self._js[destfile]:
                if self._debug:
                    f.write('{}\n'.format(self._load_js(jsfile['file'])))
                f.write(self._load_js(jsfile['file'])+';')
        print('finished')

    def minify_js(self, jsfile=None):
        """Minify JS in place, append _minified
        """
        out = jsmin(self._load_js(jsfile, load_minified=False))

        with open('{}_minified'.format(jsfile), 'w', encoding='utf-8') as f:
            f.write(out)

    def build_partial_js(self, changed):
        print('building partial js...')
        
        for minfile in self._js:
            for jsfile in self._js[minfile]:
                if changed == jsfile['file']:
                    if jsfile['minify'] and not self._debug:
                        self.minify_js(jsfile['file'])
                    self.concat_js(minfile)
        print('finished')

    def _load_js(self, jsfile, load_minified=True):
        """Load js from file, load _minifed if exists and we want to have it (we do not want it if we minify anew)
        """
        if load_minified and os.path.isfile('{}_minified'.format(jsfile)):
            jsfile = '{}_minified'.format(jsfile)

        if not os.path.isfile(jsfile):
            print(Fore.RED + 'File {} not found!'.format(jsfile))
            print(Style.RESET_ALL)

        with open(jsfile, 'r', encoding='utf-8') as f:
            out = f.read()

        return out

    def _update_timestamp(self):
        try: 
            if self._timestamp_file:
                with open(self._timestamp_file, 'w') as f:
                    f.write(int(time.time()))
                print('timesamp updated')
        except Exception as e:
            print(Fore.RED + 'Error updating timestamp file: {}'.format(e))
            print(Style.RESET_ALL)

    def build_sass(self):
        try:
            print('building sass...')
            for minfile in self._css.keys():
                with open(minfile, 'w', encoding='utf-8') as f:
                    for sassfile in self._css[minfile]:
                        if sassfile.endswith('.scss'):
                            sc = sass.compile(filename=sassfile)
                            if not self._debug:
                                sc = compress(sc)
                            f.write(sc)
                        else:
                            sc = open(sassfile, 'r', encoding='utf-8').read()
                            if not self._debug:
                                sc = compress(sc)
                            f.write(sc)
            print('finished')
            self._update_timestamp()
        except sass.CompileError as e:
            print(Fore.RED + 'SASS Error: {}'.format(e))
            print(Style.RESET_ALL)
