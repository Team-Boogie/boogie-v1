"""
This type stub file was generated by pyright.
"""

import os
import xml.etree.ElementTree as etree
from .compat_utils import passthrough_module

class compat_HTMLParseError(ValueError):
    ...


class _TreeBuilder(etree.TreeBuilder):
    def doctype(self, name, pubid, system): # -> None:
        ...
    


def compat_etree_fromstring(text): # -> Element:
    ...

def compat_ord(c): # -> int:
    ...

if os.name in ('nt', 'ce'):
    def compat_expanduser(path):
        ...
    
else:
    compat_expanduser = ...
def urllib_req_to_req(urllib_request): # -> Request:
    """Convert urllib Request to a networking Request"""
    ...

