#!/usr/bin/env python3

# Copyright © 2014-2017 Infoskærms-gruppen <infoskaerm@dikumail.dk>
#
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

# This is the control script for the informational monitors in the DIKU
# canteen, but it can be (and is) used in other places as well.  See the
# README.md file to find out how to use it.

'''
Run an infoscreen.
'''

import sys
import os
import time
import subprocess
import signal
import socket
import random
import re
import tempfile
import traceback
import atexit
import selectors
import yaml


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


_base_dir = os.path.dirname(__file__)
_socket_filename = os.path.join(_base_dir, 'kantinfo.sock')

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
        next_element = find_or_none(lambda x: x in new_list, rotate(i, old_list))
        if next_element is not None:
            return next_element

    # old_selection was not even in old_list.
    if len(new_list) == 0:
        return None
    else:
        return new_list[0]

def find_slides():
    '''
    Find the list of current slides.
    '''
    paths = [os.path.join(globs['content_directory'], f)
             for f in os.listdir(globs['content_directory'])]
    content = [p for p in paths
               if os.path.isfile(p) and
               not p.endswith(globs['config_ending'])]
    return content

def _time_to_min(t):
    if isinstance(t, int):
        return t
    else:
        h, m = map(int, t.split(':'))
        return h * 60 + m

def _time_to_sec(t):
    if isinstance(t, int):
        return t
    else:
        m, s = map(int, str(t).split(':'))
        return m * 60 + s

def _run_program(progname, args):
    print('Runs {} with arguments {}'.format(progname, args))
    proc = subprocess.Popen([progname] + args,
                            stdout=None,
                            stderr=None,
                            stdin=None,
                            close_fds=True,
                            preexec_fn=os.setsid)
    return proc

def _play_video(path):
    video_cache_dir = os.path.expanduser('~/.kantinfo-video-cache')
    start_pos = []
    end_pos = []
    try:
        intervals = globs['current_conf']['intervals']
        raw_start_pos, raw_end_pos = random.sample(intervals, 1)[0]
        start_in_seconds = _time_to_sec(raw_start_pos)
        end_in_seconds = _time_to_sec(raw_end_pos) - start_in_seconds
        start_pos = ['-ss', str(start_in_seconds)]
        end_pos = ['-endpos', str(end_in_seconds)]
    except (TypeError, KeyError):
        try:
            raw_start_pos = globs['current_conf']['start_pos']
            start_in_seconds = _time_to_sec(raw_start_pos)
            start_pos = ['-ss', str(start_in_seconds)]
        except (TypeError, KeyError):
            pass
        try:
            raw_end_pos = globs['current_conf']['end_pos']
            end_in_seconds = _time_to_sec(raw_end_pos)
            end_pos = ['-endpos', str(end_in_seconds - start_in_seconds)]
        except (TypeError, KeyError):
            pass
    try:
        os.mkdir(video_cache_dir)
    except OSError:
        pass
    if path.startswith('http://') or path.startswith('https://'):
        cur_dir = os.getcwd()
        try:
            os.chdir(video_cache_dir)
            out = subprocess.check_output(['youtube-dl',
                                           # At most 720p.  Limits space usage.
                                           '-f', '[height <=? 720]',
                                           path])
            try:
                dest = re.findall(br'\[download\] (.+?) has already been downloaded', out)[0]
            except IndexError:
                dest = re.findall(br'Destination: (.+)', out)[0]
            dest = dest.decode('utf-8')
        finally:
            os.chdir(cur_dir)
        video_path = os.path.join(video_cache_dir, dest)
    else:
        video_path = os.path.expanduser(path)

    return _run_program(os.path.join(_base_dir, 'scripts/play-video.sh'),
                       [video_path] + start_pos + end_pos)

def _show_url_in_browser(url):
    return _run_program('surf',
                       ['-p', # Disable plugins.
                        '-b', # Disable scrollbars.
                        '-d', # Disable the cache.
                        '-F', # Run in fullscreen.
                        url])

def _url_handler(url):
    if url.endswith('.mkv') or url.endswith('.webm') or url.endswith('.mp4') \
       or url.endswith('.avi') or url.endswith('.mpg') or url.endswith('.ogv') \
       or url.startswith('http://youtube.com/') \
       or url.startswith('https://youtube.com/') \
       or url.startswith('http://www.youtube.com/') \
       or url.startswith('https://www.youtube.com/') \
       or url.startswith('http://youtu.be/') \
       or url.startswith('https://youtu.be/') \
       or url.startswith('http://imgur.com/') \
       or url.startswith('https://archive.org/') \
       or url.startswith('https://vimeo.com/') \
       or url.startswith('http://vimeo.com/') \
       or url.startswith('https://www.vimeo.com/') \
       or url.startswith('http://www.vimeo.com/') \
       or url.startswith('https://dailymotion.com/') \
       or url.startswith('http://dailymotion.com/'):
        return _play_video
    else:
        return _show_url_in_browser

def _open_url(urlfile):
    with open(urlfile) as f:
        url = next(filter(lambda s: not s.startswith('#'),
                          f.read().strip().split('\n')))
    return _url_handler(url)(url)

def _show_in_browser(filename):
    return _show_url_in_browser('file://' + os.path.join(os.getcwd(), filename))

def _show_image(filename):
    return _run_program('feh',
                        ['-F', '-Z', os.path.join(os.getcwd(), filename)])

def _eval_program(filename):
    actual_file = subprocess.check_output([filename]).decode('utf-8').strip()
    if actual_file:
        return show_content(actual_file)

def _run_in_terminal(filename):
    return _run_program('lxterminal',
                        ['-e', # Start program
                         os.path.join(os.getcwd(), filename)])

def show_content(filename):
    print('Attempting to show {}'.format(filename))
    extension = os.path.splitext(filename)[1][1:]
    try:
        f = {
            'html': lambda: _show_in_browser(filename),
            'jpg': lambda: _show_image(filename),
            'png': lambda: _show_image(filename),
            'gif': lambda: _show_in_browser(filename),
            'url': lambda: _open_url(filename),
            'sh': lambda: _run_program(filename, []),
            'eval': lambda: _eval_program(filename),
            'terminal': lambda: _run_in_terminal(filename)
        }[extension]
    except KeyError:
        raise Exception('I have no idea how to show a {} file.'.format(extension))
    return f()

class Infoscreen:
    def __init__(self, do_random=False):
        self.do_random = do_random
        self.socket_filename = _socket_filename

        self.content = None
        self.content_list = []
        self.goto_next = None

    def _setup_socket(self):
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        if os.path.exists(self.socket_filename):
            os.remove(self.socket_filename)
        self.socket.bind(self.socket_filename)
        atexit.register(lambda: os.remove(self.socket_filename))
        self.socket.setblocking(False)

        self.selector = selectors.DefaultSelector()
        self.selector.register(self.socket, selectors.EVENT_READ)

    def _check_new_messages(self):
        # Return whether any new gotos were found.

        goto = None

        events = self.selector.select(0)
        for key, _mask in events:
            socket = key.fileobj
            order = socket.recv(1024) # probably large enough
            order = order.decode('utf-8')
            order = order.split()

            print(order)
            if len(order) == 2 and order[0] == 'goto':
                goto = order[1]

        if goto is not None:
            self.goto_next = goto
        return goto is not None

    def _choose_next_content(self):
        old_selection = self.content
        old_list = self.content_list
        new_list = find_slides()

        if self.goto_next is not None:
            selection = os.path.join(globs['content_directory'], self.goto_next)
            self.goto_next = None
        elif self.do_random:
            selection = random.choice(new_list)
        else:
            selection = find_next(old_selection, old_list, new_list)

        self.content = selection
        self.content_list = new_list

        return selection

    def run(self):
        '''
        Show the slides in succession.
        '''

        self._setup_socket()

        proc_prev = None
        sleep_dur_start = 1
        pull_time_prev = 0

        while True:
            content = self._choose_next_content()

            content_conf = content + globs['config_ending']
            dur = globs['duration_default']
            try:
                with open(content_conf) as f:
                    conf = f.read()
                conf = yaml.load(conf)
                globs['current_conf'] = conf
            except (IOError, yaml.YAMLError, AttributeError):
                pass
            else:
                try:
                    dur = conf['duration']
                except (TypeError, KeyError):
                    pass
                # An end point will always overrule duration.
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
                    start_at = _time_to_min(start_at)
                    end_at = _time_to_min(end_at)
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

            if self._check_new_messages():
                continue

            try:
                proc = show_content(content)
            except Exception as e:
                print('Failed to show {}:\n'.format(content))
                traceback.print_exc()
                continue

            time_start = time.time()

            # The new process has just started.  Keep the old one running for a
            # little while before killing it.
            time.sleep(sleep_dur_start)

            # Then kill it.
            if proc_prev is not None:
                # SIGKILL (or similar on other platforms)
                try:
                    os.killpg(proc_prev.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass

            # In the next iteration, the current process will become the
            # previous process.
            proc_prev = proc

            if self._check_new_messages():
                continue

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

            if self._check_new_messages():
                continue

            if proc is None:
                continue

            if dur == -1:
                # Wait for the process to terminate itself.
                while True:
                    try:
                        proc.wait(timeout=1)
                        proc_prev = None
                        break
                    except subprocess.TimeoutExpired:
                        pass
                    if self._check_new_messages():
                        break
            else:
                # Sleep for the remaining time of the duration.
                for end_cur in range(1, dur + 1):
                    elapsed = time.time() - time_start
                    dur = max(end_cur - elapsed, 0.5)
                    try:
                        proc.wait(timeout=dur)
                        proc_prev = None
                        break
                    except subprocess.TimeoutExpired:
                        pass
                    if self._check_new_messages():
                        break

def run_infoscreen(args):
    '''
    Run the infoscreen based on the list of string arguments in `args`.
    '''
    do_random = False
    if '--help' in args:
        _print_help()
        sys.exit(0)
    elif '--random' in args:
        do_random = True
        args.remove('--random')

    try:
        globs['content_directory'] = args[0]
    except IndexError:
        _print_help()
        sys.exit(0)

    try:
        filename = args[1]
    except IndexError:
        filename = None

    if filename is not None:
        # Test a file instead of waiting for it to show.
        try:
            proc = show_content(filename)
            if proc is not None:
                proc.wait()
        except KeyboardInterrupt:
            pass
    else:
        # Run the slideshow.
        try:
            while True:
                try:
                    infoscreen = Infoscreen(do_random=do_random)
                    infoscreen.run()
                except Exception:
                    print('Failed in or before main loop:\n')
                    traceback.print_exc()
                    print('Sleeping for two seconds.')
                    time.sleep(2)
        except KeyboardInterrupt:
            pass

def _print_help():
    print('kantinfo from git; see README.md for instructions')
    print()
    print('Usage:')
    print('  ./kantinfo.py CONTENT_DIRECTORY [CONTENT_FILE]')
    print()
    print('Options:')
    print('  --help    Print this text.')
    print('  --random  Show the slides in random order.')

if __name__ == '__main__':
    run_infoscreen(sys.argv[1:])
