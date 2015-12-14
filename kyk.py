
import os
import argparse

import yaml
import sass

from jsmin import jsmin


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

    def watch_forever(self):
        import pprint
        pprint.pprint(self._cfg)

        for minfile in self._cfg.keys():
            if minfile.endswith('.js'):
                self._js[minfile] = self._cfg[minfile]
            if minfile.endswith('.css'):
                self._css[minfile] = self._cfg[minfile]

        self.build_js()
        self.build_sass()


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

    def _load_sass(self, sassfile):
        with open(sassfile, 'r') as f:
            out = f.read()
        return out

    def build_sass(self):
        for minfile in self._css.keys():
            with open(minfile, 'w') as f:
                out = ''

                for sassfile in self._css[minfile]:
                    out += self._load_sass(sassfile) + "\n"
                    print(os.path.dirname(sassfile))
                    os.chdir(os.path.dirname(sassfile))  # <-- problem: 

                f.write(sass.compile(string=out))



def main():
    a = argparse.ArgumentParser()
    a.add_argument('--folder', help='folder to watch', default='.')
    args = vars(a.parse_args())

    k = Kyk(args['folder'])
    k.watch_forever()

if __name__ == '__main__':
    main()