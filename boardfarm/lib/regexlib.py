#!/usr/bin/env python3
# Copyright (c) 2018
#
# All rights reserved.
#
# This file is distributed under the Clear BSD license.
# The full text can be found in LICENSE in the root directory.

# Restrict all 4 numbers in the IP address to 0..255. It stores each of the 4
# numbers of the IP address into a capturing group. These groups can be used
# to further process the IP number.
ValidIpv4AddressRegex = r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
ValidIpv4AddressRegexWordBound = "\b" + ValidIpv4AddressRegex + "\b"

# Note: the following will match the string:
# 9.117.63.2539.117.63.253 2255.255.255.0
# as:
# (9.117.63.253) (9.117.63.253)  (255.255.255.0)
ValidIpv4AddressRegex_Nogroup = r"(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"

# IPv6 text representation of addresses without compression from RFC 1884. This
# regular expression doesn't allow IPv6 compression (&quot;::&quot;) or mixed
# IPv4 addresses.
# Matches: FEDC:BA98:7654:3210:FEDC:BA98:7654:3210 | 1080:0:0:0:8:800:200C:417A | 0:0:0:0:0:0:0:1
ValidIpv6AddressRegex = "([0-9A-Fa-f]{1,4}:){7}[0-9A-Fa-f]{1,4}"

# Below regex gives the IPv4 address and Netmask address of an Interface.
InterfaceIPv4_AddressRegex = r"inet(?:\s*addr:)?\s*([^\s]+)"
NetmaskIPv4_AddressRegex = r"ask\s?:?\s*([^\s]+)"

# Following regex gives the IPv6 address of an Interface.
InterfaceIPv6_AddressRegex = r"inet6(?:\s*addr:)?\s*([^\s]+)"

# IPv6 text representation of addresses with compression:
# Matches:
#    FEDC:BA98:7654:3210:FEDC:BA98:7654:3210
#    1080:0:0:0:8:800:200C:417A
#    0:0:0:0:0:0:0:1
#    fd42:42:42:42::1
#    1762:0:0:0:0:B03:1:AF18
#    1762:0:0:0:0:B03:127.32.67.1
#    1762::B03:1:AF18
#    762::B03:127.32.67.15
#    2001:0000:1234:0000:0000:C1C0:ABCD:0876
#    fe80:0:0:0:204:61ff:fe9d:f156
#    fe80::204:61ff:fe9d:f156
#    fe80:0000:0000:0000:0204:61ff:254.157.241.86
#    fe80:0:0:0:0204:61ff:254.157.241.86
#    fe80::204:61ff:254.157.241.86
#    ::1
#    fe80::
#    2001::
AllValidIpv6AddressesRegex = r"(?:(?:(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):){6})(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):(?:(?:[0-9a-fA-F]{1,4})))|(?:(?:(?:(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9]))\.){3}(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9])))))))|(?:(?:::(?:(?:(?:[0-9a-fA-F]{1,4})):){5})(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):(?:(?:[0-9a-fA-F]{1,4})))|(?:(?:(?:(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9]))\.){3}(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9])))))))|(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})))?::(?:(?:(?:[0-9a-fA-F]{1,4})):){4})(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):(?:(?:[0-9a-fA-F]{1,4})))|(?:(?:(?:(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9]))\.){3}(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9])))))))|(?:(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):){0,1}(?:(?:[0-9a-fA-F]{1,4})))?::(?:(?:(?:[0-9a-fA-F]{1,4})):){3})(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):(?:(?:[0-9a-fA-F]{1,4})))|(?:(?:(?:(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9]))\.){3}(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9])))))))|(?:(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):){0,2}(?:(?:[0-9a-fA-F]{1,4})))?::(?:(?:(?:[0-9a-fA-F]{1,4})):){2})(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):(?:(?:[0-9a-fA-F]{1,4})))|(?:(?:(?:(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9]))\.){3}(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9])))))))|(?:(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):){0,3}(?:(?:[0-9a-fA-F]{1,4})))?::(?:(?:[0-9a-fA-F]{1,4})):)(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):(?:(?:[0-9a-fA-F]{1,4})))|(?:(?:(?:(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9]))\.){3}(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9])))))))|(?:(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):){0,4}(?:(?:[0-9a-fA-F]{1,4})))?::)(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):(?:(?:[0-9a-fA-F]{1,4})))|(?:(?:(?:(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9]))\.){3}(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9])))))))|(?:(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):){0,5}(?:(?:[0-9a-fA-F]{1,4})))?::)(?:(?:[0-9a-fA-F]{1,4})))|(?:(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):){0,6}(?:(?:[0-9a-fA-F]{1,4})))?::))))"

# The CMTS mac-adderss format for e.g. 0025.2e34.4377
CmtsMacFormat = r"([0-9a-f]{4}\.[0-9a-fA-F]{4}\.[0-9a-f]{4})"

LinuxMacFormat = "([0-9a-f]{2}(?::[0-9a-f]{2}){5})"

WindowsMacFormat = "([0-9a-fA-F]{2}(-[0-9a-fA-F]{2}){5})"

# traceroute returns no route to ip address (i.e. '<num> * * *' 30 times)
TracerouteNoRoute = r"((.[1-9]|[1-9][0-9])(\s\s\*\s\*\s\*)(\r\n|\r|\n)){30}"

# Grep hex string format of Mac address in SNMP output
# Matches eg:F4 6D 04 61 74 E0
SNMPMacAddressRegex = r"([0-9A-Z][0-9A-Z]\s){6}"

# This following will match:
# Trying x.x.x.x...
# Connected to x.x.x.x.
# Escape character is '^]'.
telnet_ipv4_conn = ("Trying " + ValidIpv4AddressRegex +
                    r"\.\.\.\r\nConnected to " + ValidIpv4AddressRegex +
                    r"\.\r\nEscape character is '\^]'\.((\r\n){,2})")
