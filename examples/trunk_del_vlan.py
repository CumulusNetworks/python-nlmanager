#!/usr/bin/env python

import argparse
import logging
from nlmanager.nlmanager import NetlinkManager
from nlmanager.nlpacket import RTM_DELLINK

# Logging and args
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)7s: %(message)s')
log = logging.getLogger()

parser = argparse.ArgumentParser(description="Delete VLAN(s) from an interface")
parser.add_argument('ifindex', type=int, help='interface name')
parser.add_argument('vlanstart', type=int, help='vlan ID')
parser.add_argument('vlanend', type=int, help='vlan ID')
args = parser.parse_args()

# Create an instance of NetlinkManager and use it to add a subinterface
nlmanager = NetlinkManager()
nlmanager.debug_link(True)

log.info("Calling vlan_modify() with ifindex %d, vlan start %d, vlan end %d" % (args.ifindex, args.vlanstart, args.vlanend))
nlmanager.vlan_modify(RTM_DELLINK, args.ifindex, args.vlanstart, args.vlanend)
