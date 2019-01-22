#!/usr/bin/env python

import argparse
import logging
from ipaddr import IPv4Address
from nlmanager.nlmanager import NetlinkManager

"""
A basic program that uses NetlinkManager to do the equivalent of "ip route get"

root@superm-redxp-05[examples]# ip addr show eth0
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP qlen 1000
    link/ether 00:25:90:b2:01:b6 brd ff:ff:ff:ff:ff:ff
    inet 10.0.3.34/22 brd 10.0.3.255 scope global eth0
    inet6 fe80::225:90ff:feb2:1b6/64 scope link
       valid_lft forever preferred_lft forever
root@superm-redxp-05[examples]#

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

root@superm-redxp-05[examples]# ./ip_route_get.py 10.1.1.2
Prefix         nexthop    ifindex
-----------  ---------  ---------
10.1.1.2/32                     3

root@superm-redxp-05[examples]#

root@superm-redxp-05[examples]#
root@superm-redxp-05[examples]# ./ip_route_get.py 9.9.9.9
Prefix      nexthop      ifindex
----------  ---------  ---------
9.9.9.9/32  10.0.1.2           2

root@superm-redxp-05[examples]#
"""

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)7s: %(message)s')
    log = logging.getLogger()

    parser = argparse.ArgumentParser(description="Do 'ip route get' equivalent")
    parser.add_argument('ip', help='IPv4 address to lookup')
    parser.add_argument('--debug', action='store_true', help='Enable debugs', default=False)
    args = parser.parse_args()

    if args.debug:
        log.setLevel(logging.DEBUG)
        debug = True
    else:
        debug = False

    nlmanager = NetlinkManager()
    ip = IPv4Address(args.ip)

    routes = nlmanager.route_get(ip, debug=debug)
    nlmanager.routes_print(routes)
