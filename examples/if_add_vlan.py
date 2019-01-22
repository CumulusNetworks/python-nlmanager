#!/usr/bin/env python

import argparse
import logging
from nlmanager.nlmanager import NetlinkManager

"""
Example of using NetlinkManager to add a sub-interface in a vlan

root@superm-redxp-05[examples]# ip link show swp54.2
RTNETLINK answers: No such device
Cannot send link get request: No such device
root@superm-redxp-05[examples]#

root@superm-redxp-05[examples]# ./if_add_vlan.py swp54.2
2016-01-13 14:53:11,254  INFO: TXed  RTM_GETLINK, pid 7582, seq 1, 44 bytes
2016-01-13 14:53:11,254  INFO: RXed  RTM_NEWLINK, pid 7582, seq 1, 1032 bytes
2016-01-13 14:53:11,256  INFO: RXed  NLMSG_ERROR, pid 7582, seq 1, 36 bytes, error code NLE_SUCCESS...this is an ACK
2016-01-13 14:53:11,256  INFO: Calling link_add_vlan() with parent_index 56, ifname swp54.2, vlan_id 2
2016-01-13 14:53:11,263  INFO: TXed  RTM_NEWLINK, pid 7582, seq 2, 76 bytes
2016-01-13 14:53:11,263  INFO: RXed  NLMSG_ERROR, pid 7582, seq 2, 36 bytes, error code NLE_SUCCESS...this is an ACK
root@superm-redxp-05[examples]#

root@superm-redxp-05[examples]# ip link show swp54.2
93: swp54.2@swp54: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT
    link/ether 00:25:90:b2:01:fb brd ff:ff:ff:ff:ff:ff
root@superm-redxp-05[examples]#
"""

# Logging and args
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)7s: %(message)s')
log = logging.getLogger()

parser = argparse.ArgumentParser(description="Create a vlan interface")
parser.add_argument('interface', help='interface name')
args = parser.parse_args()

ifname = args.interface
(parent_ifname, vlan_id) = ifname.split('.')
vlan_id = int(vlan_id)

# Create an instance of NetlinkManager and use it to add a subinterface
nlmanager = NetlinkManager()
nlmanager.debug_link(True)
parent_index = nlmanager.get_iface_index(parent_ifname)

log.info("Calling link_add_vlan() with parent_index %d, ifname %s, vlan_id %d" % (parent_index, ifname, vlan_id))
nlmanager.link_add_vlan(parent_index, ifname, vlan_id)
