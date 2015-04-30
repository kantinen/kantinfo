#!/bin/bash

if [ -z "$DISPLAY" ] && [ $(tty) = /dev/tty1 ]; then
    while true; do
        startx
        echo "X crashed!  Restarting in ten seconds."
        sleep 10
    done
fi
