
import os
import argparse

import yaml
import sass
import pyinotify

from jsmin import jsmin
from csscompressor import compress

class Kyk(object):
    """
    Build JS
    - if min: minify in place, append _minifed
    - concat to destfile

    Build SASS:
    - compile SASS file
    - concat to destfile
    """
    
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

        self._load_config()

    def _load_config(self):
        for minfile in self._cfg.keys():
            if minfile == 'version':
                self._version = minfile:
            elif minfile.endswith('.js'):
                self._js[minfile] = self._cfg[minfile]
                self._add_to_watchlist(self._cfg[minfile])
            elif minfile.endswith('.css'):
                self._css[minfile] = self._cfg[minfile]

    def _add_to_watchlist(self, jslist):
        for f in jslist:
            fname = f
            if f.startswith('min:'):
                fname = f.split('min:')[1].strip()

            self._jswatchlist.append(os.path.abspath(fname))

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
        #if event.maskname == 'IN_MODIFY':
        #    print(event.pathname)

        if event.pathname.endswith('.scss'):
            if event.maskname == 'IN_MODIFY':
                print('{} changed!'.format(event.pathname))
                self.build_sass()

        if event.pathname in self._jswatchlist:
            if event.maskname == 'IN_MODIFY':
                print('{} changed!'.format(event.pathname))
                self.build_js()


    def build_js(self):
        """minify everything, then concat everything
        """
        print('building js...')
        for minfile in self._js.keys():
            with open(minfile, 'w') as f:
                for jsfile in self._js[minfile]:
                    if jsfile.startswith('min:'):
                        self.minify_js(jsfile.split('min:')[1].strip())

                    out = self._load_js(jsfile)

                    f.write(out)
        print('finished')

    def concat_js(self, destfile):
        print('building {}...'.format(destfile))
        with open(destfile, 'w') as f:
            for jsfile in self._js[destfile]:
                f.write(self._load_js(jsfile))
        print('finished')

    def minify_js(self, jsfile=None):
        """Minify JS in place, append _minified
        """
        if jsfile:
            out = jsmin(self._load_js(jsfile))

            with open('{}_minified'.format(jsfile), 'w') as f:
                f.write(out)

    def build_partial_js(self, changed):
        print('building partial js...')
        
        for minfile in self._js:
            for jsfile in self._js[minfile]:
                minify = False
                if jsfile.startswith('min:'):
                    tmp = jsfile.split('min:').strip()
                    minify = True
                tmp = os.path.abspath(tmp)

                if changed == tmp:
                    if minify:
                        self.minify_js(jsfile.split('min:').strip())
                    self.concat_js(minfile)
        print('finished')

    def _load_js(self, jsfile):
        """Load js from file, load _minifed if exists
        """
        if os.path.isfile('{}_minified'.format(jsfile)):
            jsfile = '{}_minified'.format(jsfile)

        with open(jsfile, 'r') as f:
            out = f.read()

        return out

    def build_sass(self):
        print('building sass...')
        for minfile in self._css.keys():
            with open(minfile, 'w') as f:
                for sassfile in self._css[minfile]:
                    f.write(compress(sass.compile(filename=sassfile)))
        print('finished')


def main():
    a = argparse.ArgumentParser()
    a.add_argument('--folder', help='folder to watch', default='.')
    args = vars(a.parse_args())

    k = Kyk(args['folder'])
    k.watch_forever()

if __name__ == '__main__':
    main()
