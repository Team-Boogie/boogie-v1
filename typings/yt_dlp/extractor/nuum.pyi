"""
This type stub file was generated by pyright.
"""

from .common import InfoExtractor

class NuumBaseIE(InfoExtractor):
    ...


class NuumMediaIE(NuumBaseIE):
    IE_NAME = ...
    _VALID_URL = ...
    _TESTS = ...


class NuumLiveIE(NuumBaseIE):
    IE_NAME = ...
    _VALID_URL = ...
    _TESTS = ...


class NuumTabIE(NuumBaseIE):
    IE_NAME = ...
    _VALID_URL = ...
    _TESTS = ...
    _PAGE_SIZE = ...


