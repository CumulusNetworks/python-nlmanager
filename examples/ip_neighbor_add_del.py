#!/usr/bin/env python

import argparse
import logging
from ipaddr import IPv4Address
from nlmanager.nlmanager import NetlinkManager, AF_INET
from nlmanager.nlpacket import Route
from pprint import pformat

"""
This program uses NetlinkManager to add or neighbors
"""

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)7s: %(message)s')
    log = logging.getLogger()

    parser = argparse.ArgumentParser(description="Add/del neighbors using nlmanager")
    parser.add_argument('--add', action='store_true', help='add routes', default=False)
    parser.add_argument('--delete', action='store_true', help='delete routes', default=False)
    # parser.add_argument('--count', help='Number of routes to add/delete', default=10)
    parser.add_argument('ifindex', type=int, help='Interface index')
    args = parser.parse_args()

    # Build a list of route tuples to add/del
    # =======================================
    ip = IPv4Address('11.1.1.1')
    mac = 'E02F.1234.1234'


    # Create an instance of NetlinkManager and
    # call neighbor_add() or neighbor_del()
    # ========================================
    nlmanager = NetlinkManager()
    nlmanager.debug_neighbor(True)

    if args.add:
        nlmanager.neighbor_add(AF_INET, args.ifindex, ip, mac)
    elif args.delete:
        nlmanager.neighbor_del(AF_INET, args.ifindex, ip, mac)
    else:
        raise Exception("You must specify --add or --delete")
