#!/bin/sh
#
# Play a video.  In a proper environment, `mplayer "$1"` would suffice, but
# `kantinfo` is typically run on ODroids, so we need a couple of hacks.

# Move the mouse away after mplayer is done.  This is necessary because of the
# SDL backend.
trap 'xdotool mousemove 2000 2000' INT QUIT TERM EXIT

# Actually play the file, but use an old SDL backend, since ODroids are silly.
video_path="$1"
start_at="$2"
end_at="$3"
mplayer -really-quiet $start_at $end_at "$video_path" -fs -vo sdl
