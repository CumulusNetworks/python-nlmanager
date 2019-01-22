#!/usr/bin/env python

import logging
from nlmanager.nlmanager import NetlinkManager

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)7s: %(message)s')
log = logging.getLogger()

nlmanager = NetlinkManager(log_level=logging.DEBUG)
nlmanager.debug_netconf(True)
nlmanager.netconf_dump()
