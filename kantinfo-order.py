#!/usr/bin/env python3

# Copyright © 2014-2016 Infoskærms-gruppen <infoskaerm@dikumail.dk>
#
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

# This is the control script for the informational monitors in the DIKU
# canteen, but it can be (and is) used in other places as well.  See the
# README.md file to find out how to use it.

'''
Send an order to a running infoscreen.
'''

import sys
import os.path
import socket
import readline


_base_dir = os.path.dirname(__file__)
_socket_filename = os.path.join(_base_dir, 'kantinfo.sock')


def send_orders(args):
    '''
    Send standard in orders based on the list of string arguments in `args`.
    '''
    if '--help' in args:
        _print_help()
        sys.exit(0)

    with socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM) as client:
        try:
            client.connect(_socket_filename)
        except FileNotFoundError:
            print('Could not find socket.')
            sys.exit(1)
        for line in sys.stdin:
            line = line.rstrip()
            order = line.encode('utf-8')
            if len(order) > 1024:
                print('Datagram too large.')
            client.send(order)

def _print_help():
    print('kantinfo from git; see README.md for instructions')
    print()
    print('Usage:')
    print('  ./kantinfo-order.py [OPTION...]')
    print()
    print('Read lines from standard in and send them to a running kantinfo.py process.')
    print()
    print('Options:')
    print('  --help    Print this text.')

if __name__ == '__main__':
    send_orders(sys.argv[1:])
