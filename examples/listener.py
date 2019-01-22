#!/usr/bin/env python

import logging
import re
import signal
import subprocess
import sys
from nlmanager.nllistener import NetlinkManagerWithListener
from nlmanager.nlpacket import *


def get_ifindex(ifname):
    output = subprocess.check_output(['/sbin/ip', 'link', 'show'])

    for line in output.splitlines():
        re_line = re.search("^(\d+): %s: " % ifname, line)
        if re_line:
            return int(re_line.group(1))
    return None


class NeighborListener(NetlinkManagerWithListener):

    def main(self):

        # This loop has two jobs:
        # - process items on our workq
        # - process netlink messages on our netlinkq, messages are placed there via our NetlinkListener
        while True:

            # Sleep until our alarm goes off...NetlinkListener will set the alarm once it
            # has placed a NetlinkPacket object on our netlinkq. If someone places an item on
            # our workq they should also set our alarm...if they don't it is not the end of
            # the world as we will wake up in 1s anyway to check to see if our shutdown_event
            # has been set.
            self.alarm.wait(1)
            self.alarm.clear()

            if self.shutdown_event.is_set():
                log.info("NeighborListener: shutting things down")
                break

            while not self.workq.empty():
                (event, options) = self.workq.get()

                if event == 'GET_ALL_ADDRESSES':
                    self.get_all_addresses()
                elif event == 'GET_ALL_LINKS':
                    self.get_all_links()
                elif event == 'GET_ALL_NEIGHBORS':
                    self.get_all_neighbors()
                elif event == 'GET_ALL_ROUTES':
                    self.get_all_routes()
                elif event == 'SERVICE_NETLINK_QUEUE':
                    self.service_netlinkq()
                else:
                    raise Exception("Unsupported workq event %s" % event)

        self.listener.shutdown_event.set()
        self.listener.join()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)7s: %(message)s')
    log = logging.getLogger()

    # groups controls what types of messages we are interested in hearing
    groups = RTMGRP_LINK | RTMGRP_NEIGH | RTMGRP_IPV4_ROUTE
    # groups = RTMGRP_ALL
    nlmanager = NeighborListener(groups)

    signal.signal(signal.SIGTERM, nlmanager.signal_term_handler)
    signal.signal(signal.SIGINT, nlmanager.signal_int_handler)

    try:
        nlmanager.listener.supported_messages_add(NLMSG_DONE)

        # Request to get all links
        nlmanager.workq.put(('GET_ALL_ADDRESSES', None))
        #nlmanager.workq.put(('GET_ALL_LINKS', None))
        #nlmanager.workq.put(('GET_ALL_NEIGHBORS', None))
        #nlmanager.workq.put(('GET_ALL_ROUTES', None))

        # Enable color coded debug output
        nlmanager.debug_address(True)
        # nlmanager.debug_link(True)
        # nlmanager.debug_neighbor(True)
        # nlmanager.debug_route(True)

        # Filtering examples
        # ==================
        # filter out neighbors on eth0
        eth0_ifindex = get_ifindex('eth0')
        nlmanager.filter_by_ifindex(True, 'blacklist', RTM_NEWNEIGH, eth0_ifindex)
        nlmanager.filter_by_ifindex(True, 'blacklist', RTM_DELNEIGH, eth0_ifindex)

        # filter netlink packets involving ipv6 neighbors or addresses
        nlmanager.filter_by_address_family(True, 'blacklist', RTM_NEWNEIGH, AF_INET6)
        nlmanager.filter_by_address_family(True, 'blacklist', RTM_DELNEIGH, AF_INET6)
        nlmanager.filter_by_address_family(True, 'blacklist', RTM_NEWADDR, AF_INET6)
        nlmanager.filter_by_address_family(True, 'blacklist', RTM_DELADDR, AF_INET6)

        '''
        # whitelist filter example
        nlmanager.filter_by_attribute(True, 'whitelist', RTM_NEWLINK, Link.IFLA_ADDRESS, '0025.90B2.01FB')

        # filtering using nested attributes
        attr_filter = {
            Link.IFLA_LINKINFO: {
                Link.IFLA_INFO_KIND: 'vlan'
            }
        }
        nlmanager.filter_by_nested_attribute(True, 'whitelist', RTM_NEWLINK, attr_filter)
        '''
        # ==================

        # NOTE: this will block
        nlmanager.main()
        sys.exit(0)

    except Exception as e:
        log.exception(e)
        nlmanager.shutdown_event.set()
        nlmanager.alarm.set()
        sys.exit(1)
