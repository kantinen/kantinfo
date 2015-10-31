#!/usr/bin/env python3

import random
import os.path
import tempfile
import subprocess


basedir = os.path.dirname(__file__)

with open(os.path.expanduser('~/breaking_news')) as f:
    breaking_news = f.read().strip()

with open(os.path.join(basedir, 'res/breaking_news_skabelon.html')) as f:
    d = f.read()

t = tempfile.NamedTemporaryFile()
fname = t.name
with open(fname, 'w') as f:
    print(d.replace('{BREAKING_NEWS}', breaking_news), file=f)

subprocess.check_call(['surf', '-p', fname])
