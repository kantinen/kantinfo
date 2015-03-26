#!/bin/bash

trap 'killall -s 9 sic; exit' INT QUIT TERM EXIT

irc_out=/tmp/diku_irc_out

usercolor='\e[0;32m'
msgcolor='\e[0;37m'

color_usermsg() {
    # Første linje af fmt-uddataen.
    read line
    start=$(echo "$line" | cut -d '>' -f 1)
    end=$(echo "$line" | cut -d '>' -f 2-)
    {
	echo -en "$usercolor"
	echo -n "$start>"
	echo -en "$msgcolor"
	echo "$end"
    }

    cat # Resterende linjer.
}

ircloop() {
    while true; do
	sic -h irc.freenode.net -n infoskaerm
    done
}

# Input til IRC-klienten.
in=$(mktemp)
touch $in

channel="#diku"

# Kør klienten i baggrunden.
{
    tail -f $in \
	| ircloop \
	| grep --line-buffered -E "^$channel" \
	| sed -ur 's/[^<]+(.+)/\1/' \
	| while IFS='' read line; do
	echo "$line" | fmt -75 | color_usermsg >> $irc_out
    done

} &

# Join #diku.
echo ":j $channel" > $in

# Wait for the client to finish.
wait
