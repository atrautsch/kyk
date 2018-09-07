Kyk
===
Simple watchscript for building minified js and css files.
Linux only as it uses pyinotify.

Watches for changes in the current directory and child directories.
It uses pyinotify for detecting changes and libsass for compiling sass files.

A example config file can be printed with kyk --yaml.

installation
------------
```bash
pip install kyk
```

quickstart
----------
```bash
# go into the directory where you want to detect changes
cd templates

# write example config
kyk --yaml > kyk.yaml

# change config
vi kyk.yaml

# run kyk
kyk
```

Options
-------
```bash
# debug, only concatenate no minification
kyk --debug

# oneshot, minify and concatenate but not watch continuously
kyk --oneshot
```


Errors
------

If something along these lines happens:
[2016-02-29 11:17:47,178 pyinotify ERROR] add_watch: cannot watch ./images WD=-1, Errno=No space left on device (ENOSPC)

It is most probably a problem with a limit.
```bash
# check max_user_watches
sysctl -n fs.inotify.max_user_watches

# set a higher number e.g. 16384
sudo sysctl -n -w fs.inotify.max_user_watches=16384
```
