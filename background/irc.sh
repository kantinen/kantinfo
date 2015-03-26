#!/bin/sh

trap 'killall sic; exit' INT QUIT TERM EXIT

irc_out=/tmp/diku_irc_out

in=$(mktemp)
touch $in
(tail -f $in | sic -h irc.freenode.net -n infoskaerm | grep --line-buffered -E '^\#diku' | sed -ur 's/[^<]+(.+)/\1/' > $irc_out) &
echo ':j #diku' > $in
wait
