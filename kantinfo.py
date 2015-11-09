#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright © 2014-2015 Infoskærms-gruppen <infoskaerm@dikumail.dk>
#
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

# This is the control script for the infoscreen in the DIKU canteen.  See the
# README.md file to find out how to use it.  This Python program is independent
# of the canteen-specific content in the repository, and you should be able to
# copy it to your own repository and add your own content, as long as you
# maintain the same directory structure.


import sys
import os
import signal
import time
import subprocess
import yaml
import time
import random


globs = {
    # The file ending used for configuration files.
    'config_ending': '.yaml',
    
    # The directory in which content is stored.
    'content_directory': 'content',

    # Whether or not to Git pull after each content switch.
    'pull_after_switch': True,

    # Default duration
    'duration_default': 20
}


def index_or_none(x, xs):
    '''
    If x is an element of xs, return its index.  Otherwise, return None.
    '''

    try:
        return xs.index(x)
    except ValueError:
        return None

def find_or_none(p, xs):
    '''
    Find the first element x in xs for which p(x) is True.  Return None if
    there is no such element.
    '''

    try:
        return filter(p, xs)[0]
    except IndexError:
        return None

def rotate(i, xs):
    '''
    Rotate/shift the list left by i positions.
    '''

    return xs[i:] + xs[:i]

def find_next(old_selection, old_list, new_list):
    '''
    If old_selection is an element of new_list, return the following element in
    new_list.

    Otherwise, if old_selection is an element of old_list, return the first
    following element in old_list that is also in new_list.

    Otherwise, if new_list is nonempty, the first element of new_list.

    Otherwise, return None.
    '''

    # First, we try to find the index of the old selection in the new
    # list.
    i = index_or_none(old_selection, new_list)
    if i is not None:
        return new_list[(i+1) % len(new_list)]

    # old_selection was not in new_list.
    i = index_or_none(old_selection, old_list)
    if i is not None:
        # Find the first element following old_list[i] that is also in
        # new_list.
        next = find_or_none(lambda x: x in new_list, rotate(i, old_list))
        if next is not None:
            return next

    # old_selection was not even in old_list.
    if len(new_list) == 0:
      return None
    else:
      return new_list[0]

def find_next_content(old_selection, old_content):
    paths = [os.path.join(globs['content_directory'], f) for f in os.listdir(globs['content_directory'])]
    new_content = [p for p in paths
                   if os.path.isfile(p) and not p.endswith(globs['config_ending'])]
    return (find_next(old_selection, old_content, new_content), new_content)

def run_program(progname, args):
    proc = subprocess.Popen([progname] + args,
                            stdout=None,
                            stderr=None,
                            stdin=None,
                            close_fds=True,
                            preexec_fn=os.setsid)
    return proc

def play_video(path):
    path = os.path.expanduser(path)
    return run_program('mplayer',
                       [path])

def show_url_in_browser(url):
    return run_program('surf',
                       ['-p', # Disable plugins.
                        url])

def url_handler(url):
    if url.endswith('.mkv') or url.endswith('.webm') or url.endswith('.mp4') \
       or url.endswith('.avi') or url.endswith('.mpg') or url.endswith('.ogv') \
       or url.startswith('https://youtube.com/'):
        return play_video
    else:
        return show_url_in_browser

def open_url(urlfile):
    with open(urlfile) as f:
        url = filter(lambda s: not s.startswith('#'),
                     f.read().strip().split('\n'))[0]
    return url_handler(url)(url)

def show_in_browser(filename):
    return show_url_in_browser('file://' + os.path.join(os.getcwd(), filename))

def show_image(filename):
    return run_program('feh',
                       ['-F', '-Z', os.path.join(os.getcwd(), filename)])

def run_in_terminal(filename):
    return run_program('lxterminal',
                       ['-e', # Start program
                        os.path.join(os.getcwd(), filename)])

def show_content(filename):
    print("Attempting to show %s" % filename)
    extension = os.path.splitext(filename)[1][1:]
    try:
        f = {
            'html': lambda: show_in_browser(filename),
            'jpg': lambda: show_image(filename),
            'png': lambda: show_image(filename),
            'gif': lambda: show_in_browser(filename),
            'url': lambda: open_url(filename),
            'sh': lambda: run_program(filename, []),
            'terminal': lambda: run_in_terminal(filename)
        }[extension]
    except KeyError:
        raise Exception("I have no idea how to show a %s file." % extension)
    return f()

def infoscreen():
    '''
    Show the slides in succession.
    '''

    proc_prev = None
    start_sleep = 1
    content = None
    content_list = []

    while True:
        try:
            if globs['pull_after_switch']:
                subprocess.call(["git", "pull"])
                
                cur_dir = os.getcwd()
                os.chdir(globs['content_directory'])
                subprocess.call(["git", "pull"])
                os.chdir(cur_dir)
        except Exception as e:
            print("Failed to git pull:\n%s" % str(e))
            time.sleep(2)

        content, content_list = find_next_content(content, content_list)
        content_conf = content + globs['config_ending']
        dur = globs['duration_default']
        try:
            with open(content_conf) as f:
                conf = f.read()
            conf = yaml.load(conf)
            conf.__getitem__
        except (IOError, yaml.YAMLError, AttributeError):
            pass
        else:
            try:
                dur = conf['duration']
            except (TypeError, KeyError):
                pass

            try:
                show_probability = conf['probability']
            except (TypeError, KeyError):
                pass
            else:
                if show_probability == 1:
                    pass
                elif random.random() >= show_probability:
                    print("The probability was not in the favor of %s." % content)
                    continue

            try:
                start_at = conf['start_at']
                end_at = conf['end_at']
            except (TypeError, KeyError):
                pass
            else:
                tloc = time.localtime()
                now = tloc.tm_hour * 60 + tloc.tm_min
                if start_at < end_at:
                    if not (start_at <= now < end_at):
                        print("Not the time for %s." % content)
                        continue
                else:
                    if end_at <= now < start_at:
                        print("Not the time for %s." % content)
                        continue

        try:
            proc = show_content(content)
        except Exception as e:
            print("Failed to show %s:\n%s" % (content, str(e)))
            print("Sleeping for two seconds.")
            time.sleep(2)

        # Kill the previous process after the current one has started.
        time.sleep(start_sleep)
        if proc_prev is not None:
            os.killpg(proc_prev.pid, signal.SIGKILL) # SIGKILL (or similar on other platforms)
        proc_prev = proc

        # Sleep more.
        time.sleep(max(0, dur - start_sleep))

if __name__ == '__main__':
    args = sys.argv[1:]

    if '--help' in args:
        print('kantinfo from git; see README.md for instructions')
        print()
        print('Usage:')
        print('  ./kantinfo.py CONTENT_DIRECTORY [CONTENT_FILE]')
        print()
        print('Options:')
        print('  --count  Count the number of slides, print it, and exit.')
        print('  --help   Print this text.')
        sys.exit(0)
    elif '--count' in args:
        paths = [os.path.join(globs['content_directory'], f)
                 for f in os.listdir(globs['content_directory'])]
        paths = [p for p in paths
                 if os.path.isfile(p) and not p.endswith(globs['config_ending'])]
        print(len(paths))
        sys.exit(0)
    else:
        globs['content_directory'] = args[0]
        
    try:
        filename = args[1]
    except IndexError:
        filename = None

    if filename is not None:
        # Test a file instead of waiting for it to show.
        try:
            proc = show_content(filename)
            proc.wait()
        except KeyboardInterrupt:
            pass
    else:
        # Run the slideshow.
        try:
            while True:
                try:
                    infoscreen()
                except Exception as e:
                    print("Failed in or before main loop:\n%s" % e)
                    print("Sleeping for two seconds.")
                    time.sleep(2)
        except KeyboardInterrupt:
            pass
