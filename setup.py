#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015,2016,2017,2018,2019 Cumulus Networks, Inc. All rights reserved
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; version 2.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#
# https://www.gnu.org/licenses/gpl-2.0-standalone.html
#
# Author:
#       Julien Fortin, julien@cumulusnetworks.com

from setuptools import setup

setup(
    version="1.0.0",
    name="nlmanager",
    description="python-nlmanager - Netlink interface using Python",
    url="https://www.cumulusnetworks.com/",
    author="Julien Fortin",
    author_email="julien@cumulusnetworks.com",
    maintainer="Julien Fortin",
    maintainer_email="julien@cumulusnetworks.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Topic :: System :: Networking",
        "Topic :: System :: Systems Administration"
    ],
    license="GNU General Public License v2",
    packages=["nlmanager"],
    install_requires=["ipaddr"],
    setup_requires=['setuptools'],
    keywords="python netlink manager nlmanager library",
)
