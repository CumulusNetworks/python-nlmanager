#!/usr/bin/env python

"""
Parse a FRR log file and replace the zlog_hexdump() output
from "debug zebra kernel msgdump" with a detailed decode of
the netlink packet
"""

import logging
import re
import sys
from nlmanager.nlmanager import NetlinkPacket
from nlmanager.nlpacket import RTM_NEWLINK, RTM_DELLINK, RTM_NEWADDR, RTM_DELADDR, RTM_NEWNEIGH, RTM_DELNEIGH, RTM_NEWROUTE, RTM_DELROUTE, Link, Address, Neighbor, Route
from struct import unpack


def print_netlink_packet(hex_data_string):

    data = hex_data_string.decode('hex')
    hex_data_string = ''

    while data:
        (length, msgtype, flags, seq, pid) = unpack(NetlinkPacket.header_PACK, data[:NetlinkPacket.header_LEN])
        print("RXed %12s, pid %d, seq %d, %d bytes" % (NetlinkPacket.type_to_string[msgtype], pid, seq, length))

        if msgtype == RTM_NEWLINK or msgtype == RTM_DELLINK:
            msg = Link(msgtype, debug=True, use_color=True)

        elif msgtype == RTM_NEWADDR or msgtype == RTM_DELADDR:
            msg = Address(msgtype, debug=True, use_color=True)

        elif msgtype == RTM_NEWNEIGH or msgtype == RTM_DELNEIGH:
            msg = Neighbor(msgtype, debug=True, use_color=True)

        elif msgtype == RTM_NEWROUTE or msgtype == RTM_DELROUTE:
            msg = Route(msgtype, debug=True, use_color=True)

        else:
            raise Exception("RXed unknown netlink message type %s" % msgtype)

        msg.decode_packet(length, flags, seq, pid, data)
        msg.dump()

        data = data[length:]


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)7s: %(message)s')
    log = logging.getLogger()


    '''
    Parse the zlog_hexdump() outpur from frr, it looks like:

    0x00007ffe3e47e0b0: 30 00 00 00 18 00 05 05 0.......
    0x00007ffe3e47e0b8: 1c 00 00 00 00 00 00 00 ........
    '''
    filename = sys.argv[1]
    hex_data_string = ''

    with open(filename, 'r') as fh:

        for line in fh:
            line = line.rstrip()
            re_line = re.search('^0x\S+: (.*) ........$', line)

            if re_line:
                data = re_line.group(1).strip().replace(' ', '')
                hex_data_string += data
            else:
                if hex_data_string:
                    print_netlink_packet(hex_data_string)
                    hex_data_string = ''
                print(line)

    if hex_data_string:
        print_netlink_packet(hex_data_string)
