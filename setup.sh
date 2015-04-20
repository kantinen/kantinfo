#!/bin/sh
#
# Setup your freshly installed ODroid distro.

set -e # Exit on first error.

if [ "$(id -u)" != 0 ]; then
    echo Run this as root.
    exit 1
fi

apt-get --yes install matchbox surf feh sic xdotool tmux

sudo -u odroid sh <<EOF
cd /home/odroid
git clone http://github.com/datalogisk-kantineforening/infoscreen.git
ln -s infoscreen/xinitrc .xinitrc
EOF

# TODO:
# Set timezone to Copenhagen.
# Set window manager to matchbox, and make it run .xinitrc on startup.
# Set crontab to reboot at 6 in the morning.

reboot
