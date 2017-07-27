Canteen's infrared display system
==========================

`Kantinfo.py` runs in a tmux on the` infoscreen` machine and `cokepc` machine
K @ ntinen - and maybe elsewhere?

See https://github.com/datalogisk-kantineforening/infoscreen and
Https://github.com/datalogisk-kantineforening/cokepc for the two most important
Systems that use the `edgeinfo` program.


Contents
-------

Supported file types and their actions:

  * `.html`,` .gif`: Appears in a browser
  * `.jpg`,` .png`: Appears in an image viewer
  * `.url`: The link in the file is opened either in a browser or in a video player,
    Depending on how the trail looks
  * `.sh`: The program is running
  * `. <Something> .eval`: The program is run and its output is saved in a temporary file
    Called `etellering. <Something>`, after which the file is run
  * `.terminal`: The program is run in a graphical terminal on the info screen


Configuration of slides
-----------------------

Each slide can have a configuration file. If a slide is called
`Et-slide.änd`, the configuration file must be called` et-slide.änd.yaml`.
The file is written in YAML format. The following fields are supported:

  * `Duration`: Takes a number in seconds and describes how long a slide should be
    see you. Standard is 20 seconds. If `duration` is -1, the script will not
    Terminate the wear, but instead wait for the wearer to terminate himself.
  * `Start_at` and` end_at` (both to be given): Describes the time of day
    Where a slide should be displayed.
  * `Probability`: Describes the likelihood that a slide will appear. Standard is
    That a slide always appears. Enter in the range 0 to 1.

Example of configuration file that ensures that a slide is displayed in only 10
seconds:

    Duration: 10

Example of configuration file that ensures that a slide is displayed only between
13 and 14:

    Start_at: 13:00
    End_at: 14:00

Sample configuration file that offers playback of random slices of a movie slideshow.
The function works with both times and full seconds.

    Intervals: [['0:00', '0:23'], ['1:04', '1:30'], [0, 500]]

Example of configuration file that offers playback of particular slices of a movie slideshow:

    Start_pos: 0:10
    End_pos: 1:40

or

    Start_pos: 41
    End_pos: 100


The order-consignment
-------------

You can send orders to a running `kantinfo.py` by driving
`Kantinfo-order.py` and give orders on the default in. `Kantinfo.py` understands
The following orders:

  * `Goto <slide>`: interrupt what happens and change as quickly as possible
    To `<slide>`.


Dependencies
-------------

`Edge info` depends on the following programs:

  + `Python`
  + `Pyyaml`: YAML library for Python
  + `Surf`: Simple browser - use any. https://github.com/Jobindex/surf
    For nicer shifts between slides
  + `Feh`: Simple image viewer
  + `Lxterminal`: Simple graphical terminal


Code Copy
-------------

Copyright © 2014-2017 Infoskerm Group <infoskaerm@dikumail.dk>

This work is free. Du kan omfordele det og / eller modify it under the
Terms of the Do What The Fuck You Want To Public License, Version 2,
As published by Sam Hocevar. See the COPYING file for more details.


Infoskærms Group
------------------

Most coded by Troels and Niels.
