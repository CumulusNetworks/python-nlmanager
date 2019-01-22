#!/usr/bin/env python

import argparse
import logging
from ipaddr import IPv4Address, IPv4Network
from nlmanager.nlmanager import NetlinkManager, AF_INET
from nlmanager.nlpacket import Route
from pprint import pformat

"""
This program uses NetlinkManager to add or delete routes...Example:

root@superm-redxp-05[examples]# ip addr show swp1
3: swp1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 500
    link/ether 00:25:90:b2:01:b7 brd ff:ff:ff:ff:ff:ff
    inet 10.1.1.1/30 scope global swp1
    inet 12.0.0.1/30 scope global swp1
    inet6 2001:10:1::1/64 scope global
       valid_lft forever preferred_lft forever
    inet6 fe80::225:90ff:feb2:1b7/64 scope link
       valid_lft forever preferred_lft forever
root@superm-redxp-05[examples]#

root@superm-redxp-05[examples]# ip route show
default via 10.0.1.2 dev eth0
10.0.0.0/22 dev eth0  proto kernel  scope link  src 10.0.3.34
10.1.1.0/30 dev swp1  proto kernel  scope link  src 10.1.1.1
10.1.1.4/30 dev swp2  proto kernel  scope link  src 10.1.1.5
12.0.0.0/30 dev swp1  proto kernel  scope link  src 12.0.0.1
12.0.0.4/30 dev swp2  proto kernel  scope link  src 12.0.0.5
12.0.0.8/30 dev swp3  proto kernel  scope link  src 12.0.0.9
12.0.0.12/30 dev swp4  proto kernel  scope link  src 12.0.0.13
12.0.0.16/30 dev swp5  proto kernel  scope link  src 12.0.0.17
12.0.0.20/30 dev swp6  proto kernel  scope link  src 12.0.0.21
20.1.1.0/24 dev swp6  proto kernel  scope link  src 20.1.1.1
40.1.1.0/30 dev swp3  proto kernel  scope link  src 40.1.1.1
40.1.1.4/30 dev swp4  proto kernel  scope link  src 40.1.1.5
40.1.1.8/30 dev swp5  proto kernel  scope link  src 40.1.1.9
root@superm-redxp-05[examples]#

root@superm-redxp-05[examples]#
root@superm-redxp-05[examples]# ./ip_route_add_del.py --add --count 10 10.1.1.2 3
2015-11-06 18:06:10,425  INFO: Routes:
[(2, IPv4Address('11.0.0.0'), 30, IPv4Address('10.1.1.2'), 3),
 (2, IPv4Address('11.0.0.4'), 30, IPv4Address('10.1.1.2'), 3),
 (2, IPv4Address('11.0.0.8'), 30, IPv4Address('10.1.1.2'), 3),
 (2, IPv4Address('11.0.0.12'), 30, IPv4Address('10.1.1.2'), 3),
 (2, IPv4Address('11.0.0.16'), 30, IPv4Address('10.1.1.2'), 3),
 (2, IPv4Address('11.0.0.20'), 30, IPv4Address('10.1.1.2'), 3),
 (2, IPv4Address('11.0.0.24'), 30, IPv4Address('10.1.1.2'), 3),
 (2, IPv4Address('11.0.0.28'), 30, IPv4Address('10.1.1.2'), 3),
 (2, IPv4Address('11.0.0.32'), 30, IPv4Address('10.1.1.2'), 3),
 (2, IPv4Address('11.0.0.36'), 30, IPv4Address('10.1.1.2'), 3)]
root@superm-redxp-05[examples]#

root@superm-redxp-05[examples]#
root@superm-redxp-05[examples]# ip route show
default via 10.0.1.2 dev eth0
10.0.0.0/22 dev eth0  proto kernel  scope link  src 10.0.3.34
10.1.1.0/30 dev swp1  proto kernel  scope link  src 10.1.1.1
10.1.1.4/30 dev swp2  proto kernel  scope link  src 10.1.1.5
11.0.0.0/30 via 10.1.1.2 dev swp1  proto xorp
11.0.0.4/30 via 10.1.1.2 dev swp1  proto xorp
11.0.0.8/30 via 10.1.1.2 dev swp1  proto xorp
11.0.0.12/30 via 10.1.1.2 dev swp1  proto xorp
11.0.0.16/30 via 10.1.1.2 dev swp1  proto xorp
11.0.0.20/30 via 10.1.1.2 dev swp1  proto xorp
11.0.0.24/30 via 10.1.1.2 dev swp1  proto xorp
11.0.0.28/30 via 10.1.1.2 dev swp1  proto xorp
11.0.0.32/30 via 10.1.1.2 dev swp1  proto xorp
11.0.0.36/30 via 10.1.1.2 dev swp1  proto xorp
12.0.0.0/30 dev swp1  proto kernel  scope link  src 12.0.0.1
12.0.0.4/30 dev swp2  proto kernel  scope link  src 12.0.0.5
12.0.0.8/30 dev swp3  proto kernel  scope link  src 12.0.0.9
12.0.0.12/30 dev swp4  proto kernel  scope link  src 12.0.0.13
12.0.0.16/30 dev swp5  proto kernel  scope link  src 12.0.0.17
12.0.0.20/30 dev swp6  proto kernel  scope link  src 12.0.0.21
20.1.1.0/24 dev swp6  proto kernel  scope link  src 20.1.1.1
40.1.1.0/30 dev swp3  proto kernel  scope link  src 40.1.1.1
40.1.1.4/30 dev swp4  proto kernel  scope link  src 40.1.1.5
40.1.1.8/30 dev swp5  proto kernel  scope link  src 40.1.1.9
root@superm-redxp-05[examples]#
root@superm-redxp-05[examples]#

root@superm-redxp-05[examples]#
root@superm-redxp-05[examples]# ./ip_route_add_del.py --del --count 10 10.1.1.2 3
2015-11-06 18:06:14,661  INFO: Routes:
[(2, IPv4Address('11.0.0.0'), 30, IPv4Address('10.1.1.2'), 3),
 (2, IPv4Address('11.0.0.4'), 30, IPv4Address('10.1.1.2'), 3),
 (2, IPv4Address('11.0.0.8'), 30, IPv4Address('10.1.1.2'), 3),
 (2, IPv4Address('11.0.0.12'), 30, IPv4Address('10.1.1.2'), 3),
 (2, IPv4Address('11.0.0.16'), 30, IPv4Address('10.1.1.2'), 3),
 (2, IPv4Address('11.0.0.20'), 30, IPv4Address('10.1.1.2'), 3),
 (2, IPv4Address('11.0.0.24'), 30, IPv4Address('10.1.1.2'), 3),
 (2, IPv4Address('11.0.0.28'), 30, IPv4Address('10.1.1.2'), 3),
 (2, IPv4Address('11.0.0.32'), 30, IPv4Address('10.1.1.2'), 3),
 (2, IPv4Address('11.0.0.36'), 30, IPv4Address('10.1.1.2'), 3)]
root@superm-redxp-05[examples]#
root@superm-redxp-05[examples]#

root@superm-redxp-05[examples]# ip route show
default via 10.0.1.2 dev eth0
10.0.0.0/22 dev eth0  proto kernel  scope link  src 10.0.3.34
10.1.1.0/30 dev swp1  proto kernel  scope link  src 10.1.1.1
10.1.1.4/30 dev swp2  proto kernel  scope link  src 10.1.1.5
12.0.0.0/30 dev swp1  proto kernel  scope link  src 12.0.0.1
12.0.0.4/30 dev swp2  proto kernel  scope link  src 12.0.0.5
12.0.0.8/30 dev swp3  proto kernel  scope link  src 12.0.0.9
12.0.0.12/30 dev swp4  proto kernel  scope link  src 12.0.0.13
12.0.0.16/30 dev swp5  proto kernel  scope link  src 12.0.0.17
12.0.0.20/30 dev swp6  proto kernel  scope link  src 12.0.0.21
20.1.1.0/24 dev swp6  proto kernel  scope link  src 20.1.1.1
40.1.1.0/30 dev swp3  proto kernel  scope link  src 40.1.1.1
40.1.1.4/30 dev swp4  proto kernel  scope link  src 40.1.1.5
40.1.1.8/30 dev swp5  proto kernel  scope link  src 40.1.1.9
root@superm-redxp-05[examples]#
"""

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)7s: %(message)s')
    log = logging.getLogger()

    parser = argparse.ArgumentParser(description="Add/del routes using nlmanager")
    parser.add_argument('--add', action='store_true', help='add routes', default=False)
    parser.add_argument('--delete', action='store_true', help='delete routes', default=False)
    parser.add_argument('--count', help='Number of routes to add/delete', default=10)
    parser.add_argument('--table', help='Kernel table to add/delete to', default=Route.RT_TABLE_MAIN)
    parser.add_argument('nexthop', help='Nexthop IP')
    parser.add_argument('nexthopifindex', help='Nexthop interface index')
    args = parser.parse_args()

    # Build a list of route tuples to add/del
    # =======================================
    routes = []
    ecmp_routes = []
    rtbase = int(IPv4Address("11.0.0.0"))
    ip = IPv4Network(rtbase)
    nexthop = IPv4Address(args.nexthop)
    nexthop_ifindex = int(args.nexthopifindex)
    ROUTE_COUNT = int(args.count)

    for x in xrange(ROUTE_COUNT):
        ip = IPv4Network(rtbase)
        rtbase += 4  # we always use /30s for this test
        routes.append((AF_INET, ip.ip, 30, nexthop, nexthop_ifindex))

    log.info("Routes:\n%s" % pformat(routes))

    # Create an instance of NetlinkManager and
    # call routes_add() or routes_del()
    # =======================================
    nlmanager = NetlinkManager()

    if args.add:
        nlmanager.routes_add(routes, ecmp_routes, table=args.table)
    elif args.delete:
        nlmanager.routes_del(routes, ecmp_routes, table=args.table)
    else:
        raise Exception("You must specify --add or --delete")
