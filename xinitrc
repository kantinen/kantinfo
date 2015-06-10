#!/bin/sh

xsetroot -solid white
export PATH=/home/odroid/bin:$PATH
xdotool mousemove 2000 2000
(sleep 5; infoscreen/background/irc.sh) &

# If X has restarted then tmux with the infoscreen script may already
# be running - if so, kill it before we start a new one.
tmux kill-session -t infoscreen

dbus-launch tmux new-session -s infoscreen -d 'cd infoscreen; ./infoscreen.py; bash'
exec matchbox-window-manager -use_titlebar no
