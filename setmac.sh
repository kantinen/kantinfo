#!/bin/sh
#
# Giv odroiden en anden MAC-adresse, så der ikke opstår konflikt med de andre
# odroids i kantinen.

while ! ip link show eth0 | grep -q c2:22:09:f2:5f:f0; do
        ip link set eth0 down
        sleep 20
        ip link set eth0 address c2:22:09:f2:5f:f0
        ip link set eth0 up
done
