#!/usr/bin/env python

import argparse
import logging
from nlmanager.nlmanager import NetlinkManager

"""
This program uses NetlinkManager to set an interface to up or down...Example:

root@superm-redxp-05[examples]# ip link show swp1
3: swp1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT qlen 500
    link/ether 00:25:90:b2:01:b7 brd ff:ff:ff:ff:ff:ff
root@superm-redxp-05[examples]#

root@superm-redxp-05[examples]# ./if_set_up_down.py --down swp1
2015-11-06 18:50:45,666  INFO: TXed  RTM_NEWLINK, pid 9429, seq 1, 40 bytes
2015-11-06 18:50:45,667  INFO: RXed  NLMSG_ERROR, pid 9429, seq 1, 36 bytes, error code NLE_SUCCESS...this is an ACK
root@superm-redxp-05[examples]#

root@superm-redxp-05[examples]# ip link show swp1
3: swp1: <BROADCAST,MULTICAST> mtu 1500 qdisc pfifo_fast state DOWN mode DEFAULT qlen 500
    link/ether 00:25:90:b2:01:b7 brd ff:ff:ff:ff:ff:ff
root@superm-redxp-05[examples]#

root@superm-redxp-05[examples]#
root@superm-redxp-05[examples]# ./if_set_up_down.py --up swp1
2015-11-06 18:50:49,758  INFO: TXed  RTM_NEWLINK, pid 9431, seq 1, 40 bytes
2015-11-06 18:50:49,759  INFO: RXed  NLMSG_ERROR, pid 9431, seq 1, 36 bytes, error code NLE_SUCCESS...this is an ACK
root@superm-redxp-05[examples]#

root@superm-redxp-05[examples]#
root@superm-redxp-05[examples]# ip link show swp1
3: swp1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT qlen 500
    link/ether 00:25:90:b2:01:b7 brd ff:ff:ff:ff:ff:ff
root@superm-redxp-05[examples]#
"""

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)7s: %(message)s')
    log = logging.getLogger()

    parser = argparse.ArgumentParser(description="Set interface up or down")
    parser.add_argument('--up', action='store_true', help='add routes', default=False)
    parser.add_argument('--down', action='store_true', help='delete routes', default=False)
    parser.add_argument('interface', help='interface name')
    args = parser.parse_args()

    nlmanager = NetlinkManager()
    if args.up:
        nlmanager.link_set_updown(args.interface, 'up')
    elif args.down:
        nlmanager.link_set_updown(args.interface, 'down')
    else:
        raise Exception("You must specify --up or --down")
