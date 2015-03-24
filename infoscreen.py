#!/usr/bin/env python
#
# Infoscreen control script.

import os
import time
import subprocess

# The directory in which content is stored.
content_directory='content'

# Whether or not to Git pull after each content switch.
pull_after_switch=True

# If x is an element of xs, return its index.  Otherwise, return None.
def index_or_none(x, xs):
    try:
        return xs.index(x)
    except ValueError:
        return None

# Find the first element x in xs for which p(x) is True.  Returns None
# if there is no such element.
def find_or_none(p, xs):
    try:
        return next(x for x in xs if p(x))
    except StopIteration:
        return None

# Rotate/shift the list left by i positions.
def rotate(i, xs):
    return xs[i:] + xs[:i]

# If old_selection is an element of new_list, return the following
# element in new_list.
#
# Otherwise, if old_selection is an element of old_list, return the
# first following element in old_list that is also in new_list.
#
# Otherwise, if new_list is nonempty, the first element of new_list.
#
# Otherwise, return None.
def find_next(old_selection, old_list, new_list):
    # First, we try to find the index of the old selection in the new
    # list.
    i = index_or_none(old_selection, new_list)
    if type(i) is int:
        return new_list[(i+1) % len(new_list)]

    # old_selection was not in new_list.
    i = index_or_none(old_selection, old_list)
    if type(i) is int:
        # Find the first element following old_list[i] that is also in
        # new_list.
        next = find_or_none(lambda x: x in new_list, rotate(i, old_list))
        if next != None:
            return next

    # old_selection was not even in old_list.
    if len(new_list) == 0:
      return None
    else:
      return new_list[0]

def find_next_content(old_selection, old_content):
    new_content = [ f for f in os.listdir(content_directory)
                    if os.path.isfile(os.path.join(content_directory,f)) ]
    return (find_next(old_selection, old_content, new_content), new_content)

def run_program_for_a_while(progname, args, a_while):
    proc = subprocess.Popen([progname] + args,
                            stdout=None,
                            stderr=None,
                            stdin=None,
                            close_fds=True)
    time.sleep(a_while)
    proc.send_signal(9) # SIGKILL

def show_in_browser(filename):
    run_program_for_a_while('surf',
                            ['-p', # Disable plugins.
                             'file://' + os.path.join(os.getcwd(), filename)],
                            20)

def show_content(filename):
    print("Attempting to show %s" % filename)
    extension = os.path.splitext(filename)[1]
    if extension == '.html':
        return show_in_browser(filename)
    if extension == '.jpg':
        return show_in_browser(filename)
    raise Exception("I have no idea how to show a %s file." % extension)

# Main command line entry point.
def infoscreen():
    content, content_list = find_next_content(None, [])
    while True:
        try:
            show_content(os.path.join(content_directory, content))
        except Exception as e:
            print("Failed to show %s:\n%s" % (content, str(e)))
            print("Sleeping for two seconds.")
            time.sleep(2)
        try:
            if pull_after_switch:
                subprocess.call(["git", "pull"])
        except Exception as e:
            print("Failed to git pull:\n%s" % str(e))
            time.sleep(2)
        content, content_list = find_next_content(content, content_list)

if __name__ == '__main__':
    while True:
        try:
            infoscreen()
        except Exception as e:
            print("Failed in or before main loop:\n%s" % e)
            print("Sleeping for two seconds.")
            time.sleep(2)
