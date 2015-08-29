#!/bin/bash

irc_out=/tmp/diku_irc_out

timecolor='\e[0;31m'
usercolor='\e[0;32m'
msgcolor='\e[0;37m'
name=infoskaerm

color_usermsg() {
    # Første linje af fmt-uddataen.
    read line
    time=$(echo "$line" | cut -d ' ' -f 1)
    user=$(echo "$line" | cut -d ' ' -f 2- | cut -d '>' -f 1)
    end=$(echo "$line" | cut -d '>' -f 2-)
    {
        echo -en "$timecolor"
        echo -en "$time "
        echo -en "$usercolor"
        echo -n "$user>"
        echo -en "$msgcolor"
        echo "$end"
    }

    cat # Resterende linjer.
}

# Input til IRC-klienten.
in=$(mktemp)
touch $in

channel="#diku"

join_channel() {
    # Join #diku.
    (echo ":j $channel" > $in) &
}

ircloop() {
    while true; do
        sic -h irc.freenode.net -n $name
        sleep 2
        join_channel
    done
}

join_channel

# Kør klienten i baggrunden.
touch $irc_out
tail -f $in \
    | ircloop \
    | grep --line-buffered -E "^$channel" \
    | gawk '{$1=$2=$3=""; print; fflush();}' \
    | tee /dev/stderr \
    | sed -u 's/^ *//' \
    | while IFS='' read line; do
          echo "$line" | fmt -75 | color_usermsg >> $irc_out
      done
