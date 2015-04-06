#!/bin/sh
#
# Kør dette script hvis du vil se infoskærmen på din egen datamat.  Hos dig
# selv, kør så:
#
#   ssh -L 5900:odroid:5900 kantine@kantine.diku.dk
#
# og i en anden terminal:
#
#   xtightvncviewer localhost

x11vnc -shared -forever -display :0
