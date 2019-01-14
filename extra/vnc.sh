#!/bin/sh
#
# Run this script on the infoscreen machine if you want to see an infoscreen on
# your own computer.  On your own machine, run:
#
#   ssh -L 5900:localhost:5900 host
#
# where 'host' is the server name -- see the README for a setup guide.  In
# another terminal on your machine, run:
#
#   xtightvncviewer localhost

x11vnc -shared -forever -display :0
