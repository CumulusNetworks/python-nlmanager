#!/usr/bin/env python

import logging
import socket
from nlmanager.nlpacket import *
from nlmanager.nlmanager import NetlinkManager

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)7s: %(message)s')
log = logging.getLogger()

nlmanager = NetlinkManager()

print "%4s  %7s  %25s  %15s" % ('AFI', 'ifindex', 'Neighbor', 'MAC')
print "%s  %s  %s  %s" % ('=' * 4, '=' * 7, '=' * 25, '=' * 15)

for msg in nlmanager.request_dump(RTM_GETNEIGH, socket.AF_UNSPEC, debug=True):

    # dump color coded debug output. This also dumps the
    # msg.attributes dictionary in human readable format
    #
    # You must set "level=logging.DEBUG" to see this output
    # msg.dump()

    print "%s  %7d  %25s  %s" %\
        ("IPv4" if msg.family == socket.AF_INET else "IPv6",
         msg.ifindex,
         msg.get_attribute_value(Neighbor.NDA_DST),
         msg.get_attribute_value(Neighbor.NDA_LLADDR))
