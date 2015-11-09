#!/bin/sh
#
# Kør dette script hvis du vil se en infoskærm på din egen datamat.  Hos dig
# selv, kør så:
#
#   ssh -L 5900:localhost:5900 host
#
# hvor 'hot' er dit navn for serveren -- se README.md for en opsætningsguide.  I
# en anden terminal hos dig selv, kør så:
#
#   xtightvncviewer localhost

x11vnc -shared -forever -display :0
