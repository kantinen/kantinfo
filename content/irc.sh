#!/bin/sh

irc_out=$HOME/diku_irc_out

echo 'Kom på IRC på #diku på irc.freenode.net!  Spørg din nabo om hjælp.'
tail -f -n 10 $irc_out
