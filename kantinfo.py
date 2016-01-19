#!/usr/bin/env python3

# Copyright © 2014-2015 Infoskærms-gruppen <infoskaerm@dikumail.dk>
#
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

# This is the control script for the informational monitors in the DIKU canteen,
# but it can be used otherwhere as well.  See the README.md file to find out how
# to use it.


import sys
import os
import signal
import time
import subprocess
import yaml
import random
import re
import traceback


globs = {
    # The file ending used for configuration files.
    'config_ending': '.yaml',

    # The directory in which content is stored.
    'content_directory': 'content',

    # Whether or not to Git pull after each content switch.
    'pull_after_switch': True,

    # Default duration
    'duration_default': 20,

    # Current conf
    'current_conf': {}
}


base_dir = os.path.dirname(__file__)

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
        return next(filter(p, xs))
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
    paths = [os.path.join(globs['content_directory'], f)
             for f in os.listdir(globs['content_directory'])]
    new_content = [p for p in paths
                   if os.path.isfile(p) and
                   not p.endswith(globs['config_ending'])]
    return (find_next(old_selection, old_content, new_content), new_content)

def run_program(progname, args):
    print(args)
    proc = subprocess.Popen([progname] + args,
                            stdout=None,
                            stderr=None,
                            stdin=None,
                            close_fds=True,
                            preexec_fn=os.setsid)
    return proc


def play_video(path):
    video_cache_dir = os.path.expanduser('~/.kantinfo-video-cache')
    start_pos = ['']
    end_pos= ['']
    try:
        intervals = globs['current_conf']['intervals']
        print(globs['current_conf'])
        [raw_start_pos, raw_end_pos] = random.sample(intervals, 1)[0]
        start_in_seconds = time_to_sec(raw_start_pos)
        end_in_seconds = time_to_sec(raw_end_pos) - start_in_seconds
        start_pos = ["-ss " + str(start_in_seconds)]
        end_pos = ["-endpos " + str(end_in_seconds)]

    except(TypeError, KeyError):
        try:
            raw_start_pos = globs['current_conf']['start_pos']
            start_in_seconds = time_to_sec(raw_start_pos)
            start_pos = ["-ss " + str(start_in_seconds)]
        except(TypeError, KeyError):
            pass
        try:
            raw_end_pos = globs['current_conf']['end_pos']
            end_in_seconds = time_to_sec(raw_end_pos)
            end_pos = ["-endpos " + str(end_in_seconds - start_in_seconds)]
        except(TypeError, KeyError):
            pass
    try:
        os.mkdir(video_cache_dir)
    except OSError:
        pass
    if path.startswith('http://') or path.startswith('https://'):
        cur_dir = os.getcwd()
        os.chdir(video_cache_dir)
        out = subprocess.check_output(['youtube-dl', path])
        try:
            dest = re.findall(br'\[download\] (.+?) has already been downloaded', out)[0]
        except IndexError:
            dest = re.findall(br'Destination: (.+)', out)[0]
        dest = dest.decode()
        os.chdir(cur_dir)
        video_path = os.path.join(video_cache_dir, dest)
    else:
        video_path = os.path.expanduser(path)

    return run_program(os.path.join(base_dir, 'scripts/play-video.sh'),
                       [video_path] + start_pos + end_pos)

def show_url_in_browser(url):
    return run_program('surf',
                       ['-p', # Disable plugins.
                        '-b', # Disable scrollbars.
                        '-F', # Run in fullscreen.
                        url])

def url_handler(url):
    if url.endswith('.mkv') or url.endswith('.webm') or url.endswith('.mp4') \
       or url.endswith('.avi') or url.endswith('.mpg') or url.endswith('.ogv') \
       or url.startswith('http://youtube.com/') or url.startswith('https://youtube.com/') \
       or url.startswith('http://www.youtube.com/') or url.startswith('https://www.youtube.com/') \
       or url.startswith('http://youtu.be/') or url.startswith('https://youtu.be/') \
       or url.startswith('http://imgur.com/'):
        return play_video
    else:
        return show_url_in_browser

def open_url(urlfile):
    with open(urlfile) as f:
        url = next(filter(lambda s: not s.startswith('#'),
                          f.read().strip().split('\n')))
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
    print('Attempting to show {}'.format(filename))
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
        raise Exception('I have no idea how to show a {} file.'.format(extension))
    return f()

def time_to_min(t):
    if isinstance(t, int):
        return t
    else:
        h, m = map(int, t.split(':'))
        return h * 60 + m

def time_to_sec(t):
    if isinstance(t, int):
        return t
    else:
        m, s = map(int, str(t).split(':'))
        return m * 60 + s



def infoscreen():
    '''
    Show the slides in succession.
    '''

    proc_prev = None
    sleep_dur_start = 1
    content = None
    content_list = []
    pull_time_prev = 0

    while True:
        content, content_list = find_next_content(content, content_list)
        content_conf = content + globs['config_ending']
        dur = globs['duration_default']
        try:
            with open(content_conf) as f:
                conf = f.read()
            conf = yaml.load(conf)
            conf.__getitem__
            globs['current_conf'] = conf
        except (IOError, yaml.YAMLError, AttributeError):
            pass
        else:
            try:
                dur = conf['duration']
            except (TypeError, KeyError):
                pass
        # An end-point will always overrule duration
            if 'end_pos' in conf or 'intervals' in conf:
                dur = -1
            try:
                show_probability = conf['probability']
            except (TypeError, KeyError):
                pass
            else:
                if show_probability == 1:
                    pass
                elif random.random() >= show_probability:
                    print('The probability was not in the favor of {}.'.format(content))
                    continue

            try:
                start_at = conf['start_at']
                end_at = conf['end_at']
            except (TypeError, KeyError):
                pass
            else:
                start_at = time_to_min(start_at)
                end_at = time_to_min(end_at)
                tloc = time.localtime()
                now = tloc.tm_hour * 60 + tloc.tm_min
                if start_at < end_at:
                    if not (start_at <= now < end_at):
                        print('Not the time for {}.'.format(content))
                        continue
                else:
                    if end_at <= now < start_at:
                        print('Not the time for {}.'.format(content))
                        continue

        try:
            proc = show_content(content)
        except Exception as e:
            print('Failed to show {}:\n'.format(content))
            traceback.print_exc()
            print('Sleeping for two seconds.')
            time.sleep(2)

        time_start = time.time()

        # The new process has just started.  Keep the old one running for a
        # little while before killing it.
        time.sleep(sleep_dur_start)

        # Then kill it.
        if proc_prev is not None:
            # SIGKILL (or similar on other platforms)
            os.killpg(proc_prev.pid, signal.SIGKILL)

        # Do the git pull while the slide is running to minimise downtime.  Only
        # pull the content repository, as pulling the code repository doesn't do
        # any good unless the script is also restarted, which will just get
        # messy.
        pull_time = time.time()
        if globs['pull_after_switch'] and \
           pull_time - pull_time_prev > 30: # Don't pull for at least 30 secs.
            pull_time_prev = pull_time
            try:
                cur_dir = os.getcwd()
                os.chdir(globs['content_directory'])
                subprocess.call(['git', 'pull'])
                os.chdir(cur_dir)
            except Exception as e:
                print('Failed to git pull:\n{}'.format(e))
                time.sleep(2)

        if dur == -1:
            # Wait for the process to terminate itself.
            proc.wait()
            proc_prev = None
        else:
            # Sleep for the remaining time of the duration.
            try:
                proc.wait(timeout=(dur - (time.time() - time_start)))
                proc_prev = None
            except subprocess.TimeoutExpired:
                proc_prev = proc

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
                except Exception:
                    print('Failed in or before main loop:\n')
                    traceback.print_exc()
                    print('Sleeping for two seconds.')
                    time.sleep(2)
        except KeyboardInterrupt:
            pass
