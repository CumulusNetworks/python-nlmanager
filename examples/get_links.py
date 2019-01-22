#!/usr/bin/env python

import logging
import socket
from nlmanager.nlpacket import *
from nlmanager.nlmanager import NetlinkManager

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)7s: %(message)s')
log = logging.getLogger()

nlmanager = NetlinkManager()


print "      Name  MAC             MTU"
print "----------  --------------  -----"

for msg in nlmanager.request_dump(RTM_GETLINK, socket.AF_UNSPEC, debug=True):

    # dump color coded debug output. This also dumps the
    # msg.attributes dictionary in human readable format
    #
    # You must set "level=logging.DEBUG" to see this output
    # msg.dump()

    print "%10s  %s  %d" % (
        msg.get_attribute_value(Link.IFLA_IFNAME),
        msg.get_attribute_value(Link.IFLA_ADDRESS),
        msg.get_attribute_value(Link.IFLA_MTU))
