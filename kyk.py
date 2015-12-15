
import os
import argparse

import yaml
import sass
import pyinotify

from colorama import init, Fore
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

    todo:
    - hooks after change event?, min as hook?
    - error handling
    - linting?
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

        init()
        self._load_config()


    def _load_config(self):
        for minfile in self._cfg.keys():
            if minfile == 'version':
                self._version = minfile:
            elif minfile.endswith('.js'):
                jsfile = self._cfg[minfile]
                minify = False
                if jsfile.startswith('min:'):
                    minify = True
                    jsfile = jsfile.split('min:')[1].strip()

                self._js[minfile] = {'file': os.path.abspath(jsfile), 'minify': minify}
                self._jswatchlist.append(os.path.abspath(jsfile))
            elif minfile.endswith('.css'):
                self._css[minfile] = self._cfg[minfile]

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

        # catch every scss file change, we can do this here because we are limited by the watchpath
        if event.pathname.endswith('.scss'):
            if event.maskname == 'IN_MODIFY':
                print('{} changed!'.format(event.pathname))
                self.build_sass()

        # catch only changes to our jsfiles
        elif event.pathname in self._jswatchlist:
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
                    if jsfile['minify']:
                        self.minify_js(jsfile['file'])

                    out = self._load_js(jsfile['file'])

                    f.write(out)
        print('finished')

    def concat_js(self, destfile):
        print('building {}...'.format(destfile))
        with open(destfile, 'w') as f:
            for jsfile in self._js[destfile]:
                f.write(self._load_js(jsfile['file']))
        print('finished')

    def minify_js(self, jsfile=None):
        """Minify JS in place, append _minified
        """
        out = jsmin(self._load_js(jsfile, load_minified=False))

        with open('{}_minified'.format(jsfile), 'w') as f:
            f.write(out)

    def build_partial_js(self, changed):
        print('building partial js...')
        
        for minfile in self._js:
            for jsfile in self._js[minfile]:
                if changed == jsfile['file']:
                    if jsfile['minify']:
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
