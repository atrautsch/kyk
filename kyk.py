
import os
import argparse

import yaml
import sass
import pyinotify

from jsmin import jsmin
from csscompressor import compress

class Kyk(object):
    
    def __init__(self, folder):
        self._folder = folder

        cfgfile = os.path.normpath(os.path.join(self._folder, 'config.yaml'))
        if not os.path.isfile(cfgfile):
            raise Exception('no config file "{}" found!'.format(cfgfile))

        with open(cfgfile, 'r') as f:
            dat = f.read()

        self._cfg = yaml.load(dat)

        self._js = {}
        self._css = {}
        self._jswatchlist = []

    def _add_to_watchlist(self, jslist):
        for f in jslist:
            fname = f
            if f.startswith('min:'):
                fname = f.split('min:')[1].strip()

            self._jswatchlist.append(os.path.abspath(fname))

    def watch_forever(self):
        # first run, build everything
        for minfile in self._cfg.keys():
            if minfile.endswith('.js'):
                self._js[minfile] = self._cfg[minfile]
                self._add_to_watchlist(self._cfg[minfile])
            if minfile.endswith('.css'):
                self._css[minfile] = self._cfg[minfile]

        self.build_js()
        self.build_sass()

        # now only changed files
        wm = pyinotify.WatchManager()
        notifier = pyinotify.Notifier(wm, default_proc_fun=self.handler)
        wm.add_watch(self._folder, pyinotify.ALL_EVENTS, rec=True, auto_add=True)
        notifier.loop()

    def handler(self, event):
        #if event.maskname == 'IN_MODIFY':
        #    print(event.pathname)

        if event.pathname.endswith('.scss'):
            if event.maskname == 'IN_MODIFY':
                print('{} changed!'.format(event.pathname))
                self.build_sass()

        if event.pathname in self._jswatchlist:
            if event.maskname == 'IN_MODIFY':
                print('{} changed!'.format(event.pathname))
                


    def build_js(self):
        for minfile in self._js.keys():
            with open(minfile, 'w') as f:
                for jsfile in self._js[minfile]:
                    if jsfile.startswith('min:'):
                        out = self._load_js(jsfile.split('min:')[1], minfy=True)
                    else:
                        out = self._load_js(jsfile)

                    f.write(out)

    def _load_js(self, jsfile, minfy=False):
        with open(jsfile, 'r') as f:
            out = f.read()

        if minfy:
            out = jsmin(out)
        return out

    def build_sass(self):
        for minfile in self._css.keys():
            with open(minfile, 'w') as f:
                for sassfile in self._css[minfile]:
                    f.write(compress(sass.compile(filename=sassfile)))



def main():
    a = argparse.ArgumentParser()
    a.add_argument('--folder', help='folder to watch', default='.')
    args = vars(a.parse_args())

    k = Kyk(args['folder'])
    k.watch_forever()

if __name__ == '__main__':
    main()