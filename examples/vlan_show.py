#!/usr/bin/env python

import argparse
import logging
from nlmanager.nlmanager import NetlinkManager
from nlmanager.nlpacket import RTM_SETLINK

# Logging and args
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)7s: %(message)s')
log = logging.getLogger()

# Create an instance of NetlinkManager and use it to add a subinterface
nlmanager = NetlinkManager()
# nlmanager.debug_link(True)
nlmanager.vlan_show()
