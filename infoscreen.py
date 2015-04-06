#!/usr/bin/env python
# encoding: utf8
#
# Infoscreen control script.

import sys
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

def run_program(progname, args):
    proc = subprocess.Popen([progname] + args,
                            stdout=None,
                            stderr=None,
                            stdin=None,
                            close_fds=True)
    return proc

def show_url_in_browser(url):
    return run_program('surf',
                       ['-p', # Disable plugins.
                        url])

def play_video(url):
    '''
    Udkommentér hvis det er for langsomt at streame video.
    '''
    # cache_dir = os.path.join(os.path.expanduser("~"), '.infoscreen-cache')
    # if not os.path.isdir(cache_dir):
    #     os.mkdir(cache_dir)
    # local = os.path.join(cache_dir, base64.b64encode(url, '+-'))
    # if not os.path.exists(local):
    #     ensure_download_video(url, local) # Takes time, but probably not too much time.
    # return run_program('mpv', ['--fullscreen', local])
    return run_program('mpv', [url])

# def ensure_download_video(url, local):
#     if url.startswith('https://youtube.com/'):
#         p = run_program('youtube-dl', ['--output', local, '--format', 'best', url])
#     else:
#         p = run_program('wget', ['--output-document', local, url])
#     p.wait()

def url_handler(url):
    if url.endswith('.mkv') or url.endswith('.webm') or url.endswith('.mp4') \
       or url.endswith('.avi') or url.endswith('.mpg') or url.endswith('.ogv') \
       or url.startswith('https://youtube.com/'):
        return play_video
    else:
        return show_url_in_browser

def open_url(urlfile):
    with open(urlfile) as f:
        url = filter(lambda s: not s.startswith('#'), f.read().strip().split('\n'))[0]
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
            'sh': lambda: run_in_terminal(filename)
        }[extension]
    except KeyError:
        raise Exception("I have no idea how to show a %s file." % extension)
    return f()

# Main command line entry point.
def infoscreen():
    content, content_list = find_next_content(None, [])
    proc_prev = None
    dur = 20
    start_sleep = 1
    while True:
        try:
            proc = show_content(os.path.join(content_directory, content))
        except Exception as e:
            print("Failed to show %s:\n%s" % (content, str(e)))
            print("Sleeping for two seconds.")
            time.sleep(2)

        # Kill the previous process after the current one has started.
        time.sleep(start_sleep)
        if proc_prev is not None:
            proc_prev.kill() # SIGKILL (or similar on other platforms)
        proc_prev = proc

        # Sleep more.
        time.sleep(max(0, dur - start_sleep))

        try:
            if pull_after_switch:
                subprocess.call(["git", "pull"])
        except Exception as e:
            print("Failed to git pull:\n%s" % str(e))
            time.sleep(2)
        content, content_list = find_next_content(content, content_list)

if __name__ == '__main__':
    try:
        filename = sys.argv[1]
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
