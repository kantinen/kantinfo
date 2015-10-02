#!/usr/bin/env python3

import random
import os.path
import tempfile
import subprocess


with open('content/res/roulette/skabelon.html') as f:
    d = f.read()

rot_time = random.randint(8, 12)
end_deg = rot_time * 139
end_res = random.randint(0, 36)
g, r, s = '<span style="color: green">grøn</span>', '<span style="color: red">rød</span>', '<span style="color: black">sort</span>'
colours = [g, r, s, r, s, r, s, r, s, r, s, s, r, s, r, s, r, s, r, r, s, r, s, r, s, r, s, r, s, s, r, s, r, s, r, s, r]
end_res = '{} {}'.format(end_res, colours[end_res])
imgpath = os.path.abspath('content/res/roulette/hjul.png')
tip = random.choice([
    'Sats alle pengene på sort!',
    'Brug din børneopsparing!',
    'Stjæl din vejleders penge!',
    'Spil hasard med dine ECTS.',
    'Kast om dig med pengesedler!',
    'SATS DET HELE PÅ 42!!!',
    'Vælg sort ELLER rød!',
    'Køb en drinks',
    'Flygt TIL Mallorca!'
])

t = tempfile.NamedTemporaryFile()
fname = t.name
with open(fname, 'w') as f:
    print(d.format(rot_time=rot_time, end_deg=end_deg, imgpath=imgpath, end_res=end_res, tip=tip),
          file=f)

subprocess.check_call(['surf', '-p', fname])
