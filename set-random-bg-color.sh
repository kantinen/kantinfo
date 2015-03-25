#!/bin/sh

xsetroot -solid "$(cat /usr/share/X11/rgb.txt | cut -d '	' -f 3- | sed 's/	//g' | tail -n +2 | sort -R | head -n 1)"
