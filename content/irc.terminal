#!/bin/bash

irc_out=/tmp/diku_irc_out

top() {
    tput cup 0 0
    echo 'Kom på IRC på #diku på irc.freenode.net!  Spørg din nabo om hjælp.' | toilet -f term --gay
}

bund() {
    tput cup 21 0
    echo -n $(echo 'Du kan f.eks. logge ind her: https://webchat.freenode.net/?channels=#diku' | toilet -f term --gay)
}

top
tail -n 1 -f $irc_out | while read line; do
    clear
    top
    tail -n 20 $irc_out
    bund
done
