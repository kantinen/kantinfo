#!/bin/sh

irc_out=/tmp/diku_irc_out

velkommen() {
    tput cup 0 0
    echo 'Kom på IRC på #diku på irc.freenode.net!  Spørg din nabo om hjælp.' | toilet -f term --gay
}

tail -f $irc_out | while read line; do
    velkommen
    tail -n 16 $irc_out
done
