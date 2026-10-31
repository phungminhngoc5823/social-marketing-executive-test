"""Stamp asset URLs in index.html with a content hash so browsers never use stale CSS/JS.

Usage: python3 -I tools/bump_version.py   (run from the repo root before committing)
"""
import hashlib
import re

css = open("assets/css/style.css", "rb").read()
js = open("assets/js/main.js", "rb").read()
v = hashlib.sha1(css + js).hexdigest()[:8]
s = open("index.html", encoding="utf-8").read()
s = re.sub(r'href="assets/css/style\.css(\?v=\w+)?"', f'href="assets/css/style.css?v={v}"', s)
s = re.sub(r'src="assets/js/main\.js(\?v=\w+)?"', f'src="assets/js/main.js?v={v}"', s)
open("index.html", "w", encoding="utf-8").write(s)
print("asset version", v)
