#!/bin/sh

xsetroot -solid white
export PATH=/home/odroid/bin:$PATH
xdotool mousemove 2000 2000
infoscreen/background/irc.sh &
dbus-launch tmux new-session -d 'cd infoscreen; ./infoscreen.py; bash'
exec matchbox-window-manager -use_titlebar no
