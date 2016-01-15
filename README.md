Kyk
===
Simple watchscript for building minified js and css files.

Watches for changes in the current directory and child directories.
It uses pyinotify for detecting changes and libsass for compiling sass files.

A example config file can be printed with kyk --yaml.

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
