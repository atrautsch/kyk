Kyk
===
- kyk.yaml
- watch for changes with inotfiy
- compile sass file
- minify and concatenate js


wichtig
-------
Auf ServerB ist es installiert aber dort wird es nicht automatisch geupdated (da der pfad zum virtualenv ein anderer ist).


uses
----
https://github.com/tikitu/jsmin
https://github.com/seb-m/pyinotify
https://github.com/dahlia/libsass-python


Beispiel Konfig
----------------

Die wird z.B. in processwire/site/templates/config.yaml abgelegt.
```
# mögliche events: alle inotify events, z.B. IN_MODIFY, IN_ATTRIB
version: 1
events:
- IN_MODIFY

./test/main.min.js:
- "test/vendor/jquery/jquery-1.11.3.min.js"
- "test/vendor/bootstrap-4.0.0-alpha.2/dist/js/bootstrap.min.js"
- "min:test/local/main.js"

# one scss includes everything, therefore we only need one
./test/main.min.css:
- "test/styles.scss"
```

Dann einfach im Ordner wo die config.yaml liegt kyk aufrufen.