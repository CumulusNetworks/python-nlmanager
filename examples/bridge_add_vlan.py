#!/usr/bin/env python

import argparse
import logging
from nlmanager.nlmanager import NetlinkManager

# Logging and args
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)7s: %(message)s')
log = logging.getLogger()

parser = argparse.ArgumentParser(description="Create a bridge vlan interface")
parser.add_argument('ifindex', type=int, help='interface name')
parser.add_argument('vlan', type=int, help='vlan ID')
args = parser.parse_args()

# Create an instance of NetlinkManager and use it to add a subinterface
nlmanager = NetlinkManager()
nlmanager.debug_link(True)

log.info("Calling link_add_bridge_vlan() with ifindex %d, vlan_id %d" % (args.ifindex, args.vlan))
nlmanager.link_add_bridge_vlan(args.ifindex, args.vlan)
