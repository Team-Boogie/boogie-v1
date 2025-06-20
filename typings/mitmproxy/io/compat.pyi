"""
This type stub file was generated by pyright.
"""

from typing import Any

"""
This module handles the import of mitmproxy flows generated by old versions.

The flow file version is decoupled from the mitmproxy release cycle (since
v3.0.0dev) and versioning. Every change or migration gets a new flow file
version number, this prevents issues with developer builds and snapshots.
"""
def convert_011_012(data):
    ...

def convert_012_013(data):
    ...

def convert_013_014(data):
    ...

def convert_014_015(data):
    ...

def convert_015_016(data):
    ...

def convert_016_017(data):
    ...

def convert_017_018(data): # -> dict[Unknown, Unknown]:
    ...

def convert_018_019(data): # -> dict[Unknown, Unknown]:
    ...

def convert_019_100(data): # -> dict[Unknown, Unknown]:
    ...

def convert_100_200(data):
    ...

def convert_200_300(data):
    ...

def convert_300_4(data):
    ...

client_connections: dict[tuple[str, ...], str] = ...
server_connections: dict[tuple[str, ...], str] = ...
def convert_4_5(data):
    ...

def convert_5_6(data):
    ...

def convert_6_7(data):
    ...

def convert_7_8(data):
    ...

def convert_8_9(data):
    ...

def convert_9_10(data):
    ...

def convert_10_11(data):
    ...

_websocket_handshakes = ...
def convert_11_12(data): # -> dict[str, Unknown]:
    ...

def convert_12_13(data):
    ...

def convert_13_14(data):
    ...

def convert_14_15(data):
    ...

def convert_15_16(data):
    ...

def convert_16_17(data):
    ...

def convert_17_18(data):
    ...

def convert_18_19(data):
    ...

def convert_19_20(data):
    ...

def convert_20_21(data):
    ...

def convert_unicode(data: dict) -> dict:
    """
    This method converts between Python 3 and Python 2 dumpfiles.
    """
    ...

converters = ...
def migrate_flow(flow_data: dict[bytes | str, Any]) -> dict[bytes | str, Any]:
    ...

