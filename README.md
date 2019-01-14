kantinfo: a simple infoscreen system
====================================

`kantinfo.py` shows slides in rotation on a screen.  It was originally
developed for the student-driven canteen at [DIKU](https://di.ku.dk/),
but is now also used elsewhere.

See https://github.com/kantinen/infoscreen for the most prominent
infoscreen using the `kantinfo` system.


Content
-------

Supported file types and their corresponding actions:

  * `.html`, `.gif`: Shown in a browser.
  * `.jpg`, `.png`: Shown in an image viewer.
  * `.url`: The URL in the file is either opened in a browser, or in a
    video player, depending on the form of the URL.
  * `.sh`: Is executed.
  * `.eval`: The executable is run, and its output is expected to be
    either a single line with a file path `something.<ext>`, which is
    then displayed according to these rules, or zero lines, which means
    that nothing is shown.
  * `.terminal`: The program is run in a graphical terminal on the screen.


Configuration of slides
-----------------------

Each slide can have a YAML file configuring it.  If a slide is called
`something.ext`, then the corresponding configuration file is located
in `something.ext.yaml` (**not** `something.yaml`, since there can be
both a `something.ext1` and a `something.ext2`).  If no configuration
file exists, then defaults are used.

The following fields are supported:

  * `duration`: Specifies how long to display the slide, in seconds.
    The default value is 20 seconds.  If the `duration` is `-1`, the
    system will not terminate the slide automatically, but rather wait
    for the slide to terminate itself.

  * `show_when`: Specifies when to display the slide.  Should contain
    a Python expression.  Can use the variables `now` of type
    `datetime.datetime`, and `now_timestamp` of type `int`.  Example:
    This will only show the slide on Tuesdays: `show_when:
    now.isoweekday() == 2`

  * `start_at` and `end_at` (both have to be specified, or neither):
    Describes when to display the slide, in a 24 hour clock format.
    Incompatible with `show_when` (performs a subset of the
    functionality of that field).

  * `probability`: Specifies the probability that a slide will be
    shown. Must be in the range 0 to 1.  The default value is `1`,
    meaning that the slides is always shown.

  * `intervals`: For video slides only.  Specifies segments from the
    video, one of which will play when the slide is shown.  Supports
    either timestamps or whole seconds.

  * `start_pos` and `end_pos`: For video slides only.  Specifies what
    part of the video to play when the slide is shown.  Supports either
    timestamps or whole seconds.

Example of a configuration that specifies, that the slide is only shown
for 10 seconds:

    duration: 10

Example of a configuration that specifies, that the slide is only shown
between 13 and 14:

    start_at: 13:00
    end_at: 14:00

Example of a configuation that specifies segments of a video to play:

    intervals: [['0:00' , '0:23'] , ['1:04', '1:30'] , [0, 500]]

Example of a configuation that specifies what part of a video to play:

    start_pos: 0:10
    end_pos: 1:40

or

    start_pos: 41
    end_pos: 100


Command interface
-------------

You can control a running instance of `kantinfo.py`, by running
`kantinfo-order.py`, and giving it commands on standard in.
`kantinfo.py` understands the following commands:

  * `goto_next`: Stop the current slide and go to the next one.
  * `goto <slide>`: Stop the current slide and go to `<slide>`.


Dependencies
-------------

`kantinfo` depends on the following software:

  + `python3`
  + `pyyaml`: YAML library for Python
  + `surf`: Simple browser -- consider using
    https://github.com/Jobindex/surf for nicer transitions between
    slides.
  + `youtube-dl`: video fetcher
  + `feh`: Simple image viewer
  + `lxterminal`: Simple graphical terminal


Copying
-------

Copyright © 2014-2019 The Infoscreen Group

This work is free. You can redistribute it and/or modify it under the
terms of the Do What The Fuck You Want To Public License, Version 2, as
published by Sam Hocevar. See the COPYING file for more details.


The Infoscreen Group
--------------------

Mostly coded by Troels and Niels.
